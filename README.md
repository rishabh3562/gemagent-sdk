---


# GemAgent

**GemAgent** is a lightweight Python SDK to build Gemini-powered agents with tool-calling capability. It provides a simple interface to run Gemini 1.5 models with custom tools and simulated event streaming.

---

## ✅ Current Features

- 🎯 Supports Google Gemini 1.5 models (via `google.generativeai`)
- 🧰 Register and use custom tools easily
- 🔁 Agent and runner system with clean separation
- 📤 Simulated streaming output (`run_streamed`)
- ✅ Simple tool call parsing using `call_tool(tool_name, arg=value)` format

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
response = asyncio.run(Runner.run(agent, "call_tool(say_hello, name='Rishabh')"))
print(response.final_output)
````

---

## 📦 Installation

```bash
pip install gemagent
```

---

## 📍 Environment

Set your Gemini API key in `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## 🚧 Roadmap (Coming Soon)

* [ ] 🔌 Native support for multiple models (OpenAI, Claude, local models)
* [ ] 🧠 Tool chaining and multi-step reasoning
* [ ] 🔄 Agent memory and context persistence
* [ ] 🎥 Real token-level streaming (for terminal and web)
* [ ] ⚙️ CLI interface and Web playground
* [ ] 📁 Plugin-style tool loading

---

## 📄 License

MIT License


## 💡 Inspiration

OpenAI recently released the [Agents SDK](https://platform.openai.com/docs/assistants/overview), which provides a powerful tool-using agent system. However, it requires a paid API key with at least $5 balance to access.

**GemAgent** was born out of the need for:

- A free, minimal alternative using **Gemini 1.5 Flash**
- Similar design and syntax to OpenAI's Agents SDK for easy migration later
- Local dev/testing without paying just to prototype tool-based agents


