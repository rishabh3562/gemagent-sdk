
# sdk/runner.py
import re, asyncio
from types import SimpleNamespace
import google.generativeai as genai
from .tools import TOOL_REGISTRY

class Runner:
    @staticmethod
    async def run(agent, message):
        prompt = agent.build_prompt(message)
        model = genai.GenerativeModel(agent.model)

        try:
            response = model.generate_content([prompt])
            text = getattr(response, "text", None)
            if not text:
                return SimpleNamespace(final_output="[No response from Gemini]")

            if "call_tool(" not in text:
                return SimpleNamespace(final_output=text.strip(), output=text.strip())

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
    async def run_streamed(agent, message):
        result = await Runner.run(agent, message)
        stream = STREAM_SIM(result.final_output)
        collected = ""
        async for event in stream.stream_events():
            delta = getattr(event.data, "delta", "")
            print(delta, end='', flush=True)
            collected += delta
        return collected

class STREAM_SIM:
    def __init__(self, full_text):
        self._tokens = re.findall(r'\w+|[^\w\s]|\s+', full_text)

    async def stream_events(self):
        for token in self._tokens:
            await asyncio.sleep(0.04)
            yield SimpleNamespace(type="delta", data=SimpleNamespace(delta=token))
