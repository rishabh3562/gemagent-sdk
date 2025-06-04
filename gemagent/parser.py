def parse_args(arg_str):
    """
    Convert a string like "key1=val1, key2=val2" into a dict:
    { "key1": "val1", "key2": "val2" }
    """
    args = {}
    for item in arg_str.split(","):
        if "=" in item:
            k, v = item.strip().split("=")
            args[k.strip()] = v.strip().strip('"').strip("'")
    return args
