from Tokenizer import *
from Node import *

class Parser:
    Toke=None
    @staticmethod
    def parseExpression():
        result=Parser.parseTerm()
        while(Parser.Toke.actual.type=="Plus" or Parser.Toke.actual.type=="Minus"):
            if(Parser.Toke.actual.value in TypeDic):
                result=BinOp(Parser.Toke.actual.value,[result,None])
                Parser.Toke.selectNext()
                result.children[1]=Parser.parseTerm()
        return result

    @staticmethod
    def parseTerm():
        result=Parser.parseFactor()
        while(Parser.Toke.actual.type=="Multiply" or Parser.Toke.actual.type=="Divide"):
            if(Parser.Toke.actual.value in TypeDic):
                result=BinOp(Parser.Toke.actual.value,[result,None])
                Parser.Toke.selectNext()
                result.children[1]=Parser.parseFactor()
          
        if(Parser.Toke.actual.type=="Number"):
            raise TypeError("Missing sign") 
    
        return result

    @staticmethod
    def parseFactor():
        result=0
        if(Parser.Toke.actual.type=="OpenP"):
            Parser.Toke.selectNext()
            result=Parser.parseExpression()
            if(Parser.Toke.actual.type=="CloseP"):
                Parser.Toke.selectNext()
                return(result)
            else:
                 raise TypeError("Missing Closed Parentesis") 

        elif(Parser.Toke.actual.type=="Plus" or Parser.Toke.actual.type=="Minus"):
            result=UnOp(Parser.Toke.actual.value,[result])
            Parser.Toke.selectNext()
            result.children[0]=Parser.parseFactor()



        elif(Parser.Toke.actual.type=="Number"):
            result=intVal(Parser.Toke.actual.value,None)
            Parser.Toke.selectNext()
        
        return result





    @staticmethod
    def run(code):
        Parser.Toke=Tokenizer(code)
        result = Parser.parseExpression()
        if(Parser.Toke.actual.type!="End"):
            raise TypeError("Finished Before EOF") 
        
        return result
