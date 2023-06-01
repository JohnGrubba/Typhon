from .warnings import error

scan_types = {
    "int": "%d",
    "string": "%s",
    "float": "%f",
    "char*": "%s",
    "bool": "%s"
}

def parse_input(assign_to: str):
    # Build Scanf Command
    variables_string = ", " + assign_to
    free_memory_string = assign_to + " = malloc(100 * sizeof(char));\n"
    return free_memory_string +f"scanf(\"%[^\\n]%*c\"{variables_string});\n"