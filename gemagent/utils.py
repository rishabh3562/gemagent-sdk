from contextlib import contextmanager

@contextmanager
def trace(label: str):
    """
    Context manager to print a start/finish trace for a block.
    Usage:
        with trace("MyTask"):
            # do something
    """
    print(f"▶︎ {label} …")
    try:
        yield
    finally:
        print(f"✔︎ {label} done.")
