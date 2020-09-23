import sys
import re

from Parser import Parser

def main():
    path=sys.argv[1]
    path=open(path,"r").read()
    result = Parser.run(path)
    print(result.Evaluate())
    return result



main()