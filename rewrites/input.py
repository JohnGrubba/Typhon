from .warnings import error

scan_types = {
    "int": "%d",
    "string": "%s",
    "float": "%f",
    "char*": "%s",
    "bool": "%s",
    "double": "%lf",
}

def parse_input(assign_to: str, scan_type: str, line_no: int):
    # Build Scanf Command
    variables_string = ", &" + assign_to
    format_string = scan_types.get(scan_type, None)
    if not format_string:
        error(f"Error on input() in Line {line_no}: Unknown datatype")
    free_memory_string = ""
    if scan_type == "char*":
        free_memory_string = assign_to + " = malloc(100 * sizeof(char));\n"
        variables_string = ", " + assign_to
        format_string = "%[^\\n]%*c"
    return free_memory_string +f"scanf(\"{format_string}\"{variables_string});\n"