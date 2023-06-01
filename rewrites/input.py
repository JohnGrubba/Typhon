from .warnings import error

scan_types = {
    "int": "%d",
    "string": "%s",
    "float": "%f",
    "char*": "%s",
    "bool": "%s"
}

def parse_input(assign_to: str, scan_type: str):
    # Build Scanf Command
    variables_string = ", &" + assign_to
    format_string = scan_types.get(scan_type)
    free_memory_string = ""
    if scan_type == "char*":
        free_memory_string = assign_to + " = malloc(100 * sizeof(char));\n"
        variables_string = ", " + assign_to
        format_string = "%[^\\n]%*c"
    return free_memory_string +f"scanf(\"{format_string}\"{variables_string});\n"