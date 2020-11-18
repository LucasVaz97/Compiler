import sys
import re
from WriteAssembly import Compiler

from Parser import Parser

def main():
    path=sys.argv[1]
    path=open(path,"r").read()
    result = Parser.Run(path)
    Compiler.AddInstruction("""; interrupcao de saida
    POP EBP
    MOV EAX, 1
    INT 0x80
    """)
    Compiler.WriteFile()
    return result

main()