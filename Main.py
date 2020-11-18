import sys
import re
from WriteAssembly import Compiler

from Parser import Parser

def main():
    path=sys.argv[1]
    path=open(path,"r").read()
    result = Parser.Run(path)
    Compiler.WriteFile()
    return result

main()