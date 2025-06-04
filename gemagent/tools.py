TOOL_REGISTRY = {}

def tool_custom(func=None, *, name=None):
    """
    Decorator to register a function as a tool.
    Usage:
        @tool_custom
        def my_tool(...): ...
    """
    def wrapper(fn):
        TOOL_REGISTRY[name or fn.__name__] = fn
        return fn
    return wrapper(func) if func else wrapper

@tool_custom
def say_hello(name="world"):
    """Simple tool that greets."""
    return f"Hello, {name} from tool!"

@tool_custom
def word_count(text=""):
    """Returns word count."""
    return f"Word count: {len(text.split())}"
