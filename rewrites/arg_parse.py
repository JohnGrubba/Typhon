def argument_parser(args: str, variables: dict):
    args = [x.strip().lstrip() for x in args]
    types = []
    for arg in args:
        if arg in variables.keys():
            types.append((variables[arg], arg))
        else:
            types.append(arg.replace('"', "").replace("'", ""))
    return types