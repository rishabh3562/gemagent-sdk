# GemAgent

GemAgent is a lightweight Python SDK to build Gemini-powered agents with tool-calling capability.

---

## ✅ Current Features

- 🎯 Supports Google Gemini 1.5 models (via `google.generativeai`)
- 🧰 Register and use custom tools easily
- 🔁 Agent and runner system with clean separation
- 📤 Simulated streaming output (`run_streamed`)
- ✅ Simple tool call parsing using `call_tool(tool_name, arg=value)` format

---

## 💡 Inspiration

OpenAI recently released the [Agents SDK](https://platform.openai.com/docs/assistants/overview), which requires a paid API key (minimum \$5 deposit).  
**GemAgent** was born to provide a **free, minimal alternative** using **Gemini 1.5 Flash**, with a similar design so you can migrate later. Local prototyping without constant billing.

---

## 🔧 Example Usage

```python
from gemagent import Agent, Runner, tool_custom

@tool_custom
def say_hello(name="world"):
    return f"Hello, {name}!"

agent = Agent(
    name="DemoAgent",
    instructions="Be helpful and use tools if needed.",
    tools=[say_hello],
)

import asyncio

res = asyncio.run(Runner.run(agent, "call_tool(say_hello, name='Rishabh')"))
print(res.final_output)
