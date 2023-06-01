import os
import re, argparse

datatypes = {
    "int": "int",
    "string": "char*",
    "float": "float",
    "double": "double",
    "char": "char",
    "bool": "bool"
}

statements = {
    ("print", r'print\(([^)]+)\)'): "printf",
}
print_types = {
    "int": "%d",
    "string": "%s",
    "float": "%f",
    "char*": "%s",
    "bool": "%d"
}

variables = {}

def argument_parser(args: str):
    args = [x.strip().lstrip() for x in args]
    types = []
    for arg in args:
        if arg in variables.keys():
            types.append((variables[arg], arg))
        else:
            types.append(arg.replace('"', "").replace("'", ""))
    return types

def compile_line(line: str, line_no: int):
    if line == "\n":
        return line
    for statement in [(re.sub(x[1], r'\1', line), x[0], statements[x]) for x in statements.keys() if re.search(x[1], line)]:
        # Statement description
        # Statement[0] = arguments
        # Statement[1] = original function name
        # Statement[2] = new function name
        if statement[2] == "printf":
            # Build Printf Command
            arguments = statement[0].split(',')
            parsed_args = argument_parser(arguments)
            format_string = ""
            for types in parsed_args:
                if type(types) == tuple:
                    format_string += print_types[types[0]]
                else:
                    format_string += types
            variables_string = ""
            for types in parsed_args:
                if type(types) == tuple:
                    variables_string += ", " + types[1]
            return f"{statement[2]}(\"{format_string}\"{variables_string});\n"
        return f"{statement[2]}(\"{print_types[variables[statement[0]]]}\", {statement[0]});\n"
    
    splitted_line = [x.strip() for x in re.split(':|=', line)]
    for datatype in datatypes.keys():
        splitted_line[1] = splitted_line[1].replace(datatype, datatypes[datatype])
    if not variables.get(splitted_line[0], None):
        # We have a new variable (save type)
        variables[splitted_line[0]] = splitted_line[1]
        return f"{splitted_line[1]} {splitted_line[0]} = {splitted_line[2]};\n"
    else:
        # Variable already existing (typecheck)
        if len(splitted_line) > 2:
            raise Exception(f"Error in Line {line_no}: Variable already existing")
        return f"{splitted_line[0]} = {splitted_line[1]};\n"
    

def main():
    # Parse Arguments
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('filename', metavar='path', type=str)
    parser.add_argument('-o', metavar='path', type=str, required=False)
    parser.add_argument('--dev', action='store_true')
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    try:
        filename = str(args.filename)
    except:
        raise Exception('No filename provided')
    if args.o:
        output_filename = args.o
    else:
        output_filename = filename.split('.')[0]
    code_lines = open(filename, 'r').readlines()
    output = "#include <stdio.h>\n\nint main(void){\n"
    for line, line_no in zip(code_lines, range(1, len(code_lines)+1)):
        output += compile_line(line, line_no)
    output += "return 0;\n}"
    # Compute Temp Filename
    tempc_filename = "temp.c"
    open(tempc_filename, 'w').write(output)
    os.system("gcc " + tempc_filename + " -o " + output_filename)
    if not args.dev:
        os.remove(tempc_filename)
    if args.run:
        os.execl(output_filename)

if __name__ == '__main__':
    main()