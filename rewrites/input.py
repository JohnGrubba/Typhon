from .warnings import error

scan_types = {
    "int": "%d",
    "string": "%s",
    "float": "%f",
    "char*": "%s",
    "bool": "%s"
}

def parse_input(parsed_args: tuple, line_no: int):
    # Build Scanf Command
    format_string = ""
    for types in parsed_args:
        if type(types) == tuple:
            try:
                format_string += scan_types[types[0]]
            except KeyError:
                error(f"Error in Line {line_no}: Unknown datatype")
        else:
            format_string += types
    variables_string = ""
    for types in parsed_args[::-1]:
        if type(types) == tuple:
            variables_string += ", " + types[1]
    free_memory_string = "input_str = malloc(100 * sizeof(char));\n"
    return free_memory_string +f"scanf(\"{format_string}\"{variables_string});\n"