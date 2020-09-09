import sys
import re

from Parser import Parser

def main():
    code=sys.argv[1]
    result = Parser.run(code)
    print(result)
    return result



main()