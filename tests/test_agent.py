import pytest
import asyncio
from gemagent.agent import Agent, Runner
from gemagent.tools import say_hello

@pytest.mark.asyncio
async def test_say_hello_tool():
    assert say_hello(name="Test") == "Hello, Test from tool!"

@pytest.mark.asyncio
async def test_agent_without_tool(monkeypatch):
    # Monkey-patch Gemini model to return a simple text
    class DummyResponse:
        text = "Just a plain response."

    class DummyModel:
        def __init__(self, model_name):
            pass
        def generate_content(self, prompts):
            return DummyResponse()

    monkeypatch.setattr("google.generativeai.GenerativeModel", DummyModel)

    agent = Agent(name="TestAgent", instructions="", tools=[])
    res = await Runner.run(agent, "Hello without tool")
    assert res.final_output == "Just a plain response."

@pytest.mark.asyncio
async def test_agent_with_tool(monkeypatch):
    # Monkey-patch Gemini to respond with a call_tool pattern
    class DummyResponse:
        text = "call_tool(say_hello, name='Tester')"

    class DummyModel:
        def __init__(self, model_name):
            pass
        def generate_content(self, prompts):
            return DummyResponse()

    monkeypatch.setattr("google.generativeai.GenerativeModel", DummyModel)

    agent = Agent(name="TestAgent", instructions="", tools=[say_hello])
    res = await Runner.run(agent, "Trigger tool")
    assert res.final_output == "Hello, Tester from tool!"
