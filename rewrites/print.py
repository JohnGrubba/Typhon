from .warnings import error

print_types = {
    "int": "%d",
    "string": "%s",
    "float": "%f",
    "char*": "%s",
    "bool": "%s"
}

def parse_print(parsed_args: tuple, line_no: int):
    # Build Printf Command
    format_string = ""
    for types in parsed_args:
        if type(types) == tuple:
            try:
                format_string += print_types[types[0]]
            except KeyError:
                error(f"Error in Line {line_no}: Unknown datatype")
        else:
            format_string += types
    variables_string = ""
    for types in parsed_args:
        if type(types) == tuple:
            if types[0] == "bool":
                variables_string += ", " + types[1] + " ? \"true\" : \"false\""
            variables_string += ", " + types[1]
    return f"printf(\"{format_string}\"{variables_string});\n"