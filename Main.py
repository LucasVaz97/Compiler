import sys
import re

from Parser import Parser

def main():
    path=sys.argv[1]
    path=open(path,"r").read()
    result = Parser.Run(path)
    return result

main()