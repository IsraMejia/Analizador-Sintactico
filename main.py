from Lexer import *
from parser_1 import *
import sys



def main():
    print("\n\t\tParser . Proyecto 2 compiladores")

    if len(sys.argv) != 2:
        sys.exit("Error: el compilador necesita el archivo fuente como argumento.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    
    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.programa() 
    print()

main()