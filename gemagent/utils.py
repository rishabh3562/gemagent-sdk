# sdk/utils.py
from contextlib import contextmanager

@contextmanager
def trace(label: str):
    print(f"▶︎ {label} …")
    try:
        yield
    finally:
        print(f"✔︎ {label} done.")

# def parse_args(arg_str):
#     args = {}
#     for item in arg_str.split(","):
#         if "=" in item:
#             k, v = item.strip().split("=")
#             args[k.strip()] = v.strip().strip('"').strip("'")
#     return args
