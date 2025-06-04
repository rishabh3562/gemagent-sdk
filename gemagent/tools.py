#  sdk/tools.py

TOOL_REGISTRY = {}

def tool_custom(func=None, *, name=None):
    def wrapper(fn):
        TOOL_REGISTRY[name or fn.__name__] = fn
        return fn
    return wrapper(func) if func else wrapper

@tool_custom
def say_hello(name="world"):
    """Simple tool that greets."""
    return f"Hello, {name} from tool!"

# TOOL_REGISTRY = {}

# def tool_custom(func=None, *, name=None):
#     def wrapper(fn):
#         TOOL_REGISTRY[name or fn.__name__] = fn
#         return fn
#     return wrapper(func) if func else wrapper

# @tool_custom
# def say_hello(name="world"):
#     """Simple tool that greets."""
#     return f"Hello, {name} from tool!"
