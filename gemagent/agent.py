import re
from types import SimpleNamespace
import google.generativeai as genai
from gemagent.tools import TOOL_REGISTRY
from gemagent.parser import parse_args
from gemagent.stream import STREAM_SIM
from gemagent.config import configure
class Agent:
    """
    Core Agent class defining name, instructions, model, tools, etc.
    """
    def __init__(self, *, name, instructions="", model="gemini-1.5-flash",
                 tools=None, verbose=False, temperature=0.7, max_tokens=1000,
                 metadata=None, async_callback=None):
        self.name = name
        self.instructions = instructions.strip()
        self.model = model
        self.tools = tools or []
        self.verbose = verbose
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.metadata = metadata or {}
        self.async_callback = async_callback
        # configure(api_key)
    def build_prompt(self, user_input: str) -> str:
        """
        Construct the full prompt including tool list and user input.
        """
        tool_list = "\n".join(
            f"- {tool.__name__}: {tool.__doc__ or 'No description'}"
            for tool in self.tools
        )
        return f"""
You are {self.name}.
{self.instructions}

You can use the following tools:
{tool_list}

If you need a tool, use: `call_tool(tool_name, arg=value)`
Otherwise, just answer normally.

User message:
{user_input.strip()}
"""

class Runner:
    """
    Runner with two static methods:
      - run: synchronous Gemini call with optional tool invocation
      - run_streamed: simulate streaming output
    """
    @staticmethod
    async def run(agent: Agent, message: str) -> SimpleNamespace:
        prompt = agent.build_prompt(message)
        model = genai.GenerativeModel(agent.model)

        try:
            response = model.generate_content([prompt])
            text = getattr(response, "text", None)
            if not text:
                return SimpleNamespace(final_output="[No response from Gemini]")

            # If no tool call pattern, return raw text
            if "call_tool(" not in text:
                return SimpleNamespace(final_output=text.strip(), output=text.strip())

            # Parse and execute first tool call found
            matches = re.findall(r"call_tool\((\w+),\s*([^)]*)\)", text)
            if matches:
                for tool_name, raw_args in matches:
                    args = parse_args(raw_args)
                    tool_fn = TOOL_REGISTRY.get(tool_name)
                    if tool_fn:
                        result = tool_fn(**args)
                        return SimpleNamespace(final_output=str(result), output=str(result))
                return SimpleNamespace(final_output=f"[Tool not found: {tool_name}]")

            return SimpleNamespace(final_output=text.strip(), output=text.strip())

        except Exception as e:
            return SimpleNamespace(final_output=f"[Gemini API error: {e}]")

    @staticmethod
    async def run_streamed(agent: Agent, message: str):
        """
        Use run() to get full text, then simulate streaming token-by-token.
        """
        result = await Runner.run(agent, message)
        stream = STREAM_SIM(result.final_output)
        collected = ""
        async for event in stream.stream_events():
            delta = getattr(event.data, "delta", "")
            print(delta, end="", flush=True)
            collected += delta
        return collected
