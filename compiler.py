import os, timeit
import re, argparse

from rewrites.print import parse_print
from rewrites.input import parse_input
from rewrites.warnings import warning, error
from rewrites.arg_parse import argument_parser

datatypes = {
    "int": "int",
    "string": "char*",
    "char*": "char*",
    "float": "float",
    "double": "double",
    "char": "char",
    "bool": "bool"
}

statements = {
    ("print", r'print\(([^)]+)\)'): "printf",
    ("input", r'input\(([^)]+)\)'): "scanf",
}

variables = {}

def compile_line(line: str, line_no: int):
    if line == "\n":
        return ""
    splitted_line = [x.strip() for x in re.split(':|=', line)]
    for statement in [(re.findall(x[1], line), x[0], statements[x]) for x in statements.keys() if x[0] in line]:
        # Statement description
        # Statement[0] = arguments
        # Statement[1] = original function name
        # Statement[2] = new function name
        arguments = []
        if not len(statement[0]) == 0:
            arguments = statement[0][0].split(',')
        parsed_args = argument_parser(arguments, variables)
        # Typecheck
        if statement[2] == "printf":
            return parse_print(parsed_args, line_no)
        elif statement[2] == "scanf":
            decl = ""
            if not variables.get(splitted_line[0], None):
                datatyp = "char*"
                if datatypes.get(splitted_line[1], None):
                    datatyp = datatypes[splitted_line[1]]
                decl = f"{datatyp} {splitted_line[0]};\n"
                variables[splitted_line[0]] = datatyp
            # Print before scan (like in python)
            prnt = ""
            if len(parsed_args) >= 1:
                prnt = parse_print(parsed_args, line_no)
            return prnt + decl + parse_input(splitted_line[0], variables[splitted_line[0]], line_no)

    if len(splitted_line) <= 1:
        error(f"Error in Line {line_no}: Invalid Syntax")
    for datatype in datatypes.keys():
        splitted_line[1] = splitted_line[1].replace(datatype, datatypes[datatype])
    if not variables.get(splitted_line[0], None):
        # We have a new variable (save type)
        if not datatypes.get(splitted_line[1], None):
            error(f"Error in Line {line_no}: Unknown datatype \"{splitted_line[1]}\"")
        if datatypes.get(splitted_line[0], None):
            error(f"Error in Line {line_no}: You can't name a variable like a datatype")
        variables[splitted_line[0]] = splitted_line[1]
        if len(splitted_line) > 2:
            return f"{splitted_line[1]} {splitted_line[0]} = {splitted_line[2]};\n"
        else:
            warning("Warning in Line " + str(line_no) + ": Variable not initialized (weird behaviour expected)")
            return f"{splitted_line[1]} {splitted_line[0]};\n"
    else:
        # Variable already existing (typecheck)
        if len(splitted_line) > 2:
            error(f"Error in Line {line_no}: Variable already existing")
        return f"{splitted_line[0]} = {splitted_line[1]};\n"
    

def main():
    # Parse Arguments
    parser = argparse.ArgumentParser(description='Typhon Compiler')
    parser.add_argument('filename', metavar='path', type=str, help="Input Filename (.ty)")
    parser.add_argument('-o', metavar='path', type=str, required=False, help="Output Filename")
    parser.add_argument('--dev', action='store_true', help="Keeps the temp.c file")
    parser.add_argument('--run', action='store_true', help="Runs the compiled code after compilation")
    parser.add_argument('--metrics', action='store_true', help="Prints some metrics about the compiled code")
    args = parser.parse_args()
    try:
        filename = str(args.filename)
    except:
        raise Exception('No filename provided')
    if args.o:
        output_filename = args.o
    else:
        output_filename = filename.split('.')[0] + ".out"
    try:
        code_lines = open(filename, 'r').readlines()
    except FileNotFoundError:
        error("Input File not found!")
    start_time = timeit.default_timer()
    # Detect Possible Libraries
    output = "#include <stdio.h>\n"
    if "bool" in "".join(code_lines):
        output += "#include <stdbool.h>\n"
    if "input" in "".join(code_lines):
        output += "#include <stdlib.h>\n"

    output += "\nint main(void){\n"
    for line, line_no in zip(code_lines, range(1, len(code_lines)+1)):
        output += compile_line(line, line_no)
    output += "return 0;\n}"
    # Compute Temp Filename
    tempc_filename = "temp.c"
    open(tempc_filename, 'w').write(output)
    os.system("gcc " + tempc_filename + " -o " + output_filename + " -w")
    # Compilation (Preprocessing) is done
    if args.metrics:
        variables_count = len(variables.keys())
        print(f"Variables used: {variables_count}")
        print(f"Lines of Code: {len(code_lines)}")
        print(f"Time: {round(timeit.default_timer() - start_time, 2)}s")
    if not args.dev:
        os.remove(tempc_filename)
    if args.run:
        os.execl(output_filename, output_filename)

if __name__ == '__main__':
    main()