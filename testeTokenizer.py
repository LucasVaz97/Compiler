from Tokenizer import *
import sys

path=sys.argv[1]
path=open(path,"r").read()

toke=Tokenizer(path)

while(toke.actual.type != "EOF"):
    print("Value: {}  Type: {}".format(toke.actual.value,toke.actual.type))
    toke.selectNext()
