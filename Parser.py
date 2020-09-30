from Tokenizer import *
from Node import *

class Parser:
    Toke=None


    @staticmethod
    def Block():
        while(Parser.Toke.actual.type!="End"):
            result=Parser.Command()
            Parser.Toke.selectNext()

        return result

    @staticmethod
    def Command():
        if(Parser.Toke.actual.type=="Command"):
            if(Parser.Toke.actual.value=="println"):
                Parser.Toke.selectNext()
                result=Parser.ParseExpression().Evaluate()
                print(result)
        elif(Parser.Toke.actual.type=="Variable"):
            Variable=Parser.Toke.actual.value
            Parser.Toke.selectNext()
            if(Parser.Toke.actual.value=="="):
                Parser.Toke.selectNext()
                value=Parser.ParseExpression().Evaluate()
                SetEqual("=",[Variable,value]).Evaluate()

        else:
            raise ValueError("Invalid expression: Declare a variable or call a Command")
                        
    @staticmethod
    def ParseExpression():
        result=Parser.ParseTerm()
        while(Parser.Toke.actual.type=="Plus" or Parser.Toke.actual.type=="Minus"):
            if(Parser.Toke.actual.value in TypeDic):
                result=BinOp(Parser.Toke.actual.value,[result,None])
                Parser.Toke.selectNext()
                result.children[1]=Parser.ParseTerm()
        return result

    @staticmethod
    def ParseTerm():
        result=Parser.ParseFactor()
        while(Parser.Toke.actual.type=="Multiply" or Parser.Toke.actual.type=="Divide"):
            if(Parser.Toke.actual.value in TypeDic):
                result=BinOp(Parser.Toke.actual.value,[result,None])
                Parser.Toke.selectNext()
                result.children[1]=Parser.ParseFactor()
          
        if(Parser.Toke.actual.type=="Number"):
            raise TypeError("Missing sign") 
    
        return result

    @staticmethod
    def ParseFactor():
        result=0
        if(Parser.Toke.actual.type=="OpenP"):
            Parser.Toke.selectNext()
            result=Parser.ParseExpression()
            if(Parser.Toke.actual.type=="CloseP"):
                Parser.Toke.selectNext()
                return(result)
            else:
                 raise TypeError("Missing Closed Parentesis") 

        elif(Parser.Toke.actual.type=="Plus" or Parser.Toke.actual.type=="Minus"):
            result=UnOp(Parser.Toke.actual.value,[result])
            Parser.Toke.selectNext()
            result.children[0]=Parser.ParseFactor()

        elif(Parser.Toke.actual.type=="Number"):
            result=intVal(Parser.Toke.actual.value,None)
            Parser.Toke.selectNext()

        elif(Parser.Toke.actual.type=="Variable"):
            result=Val(Parser.Toke.actual.value,None)
            Parser.Toke.selectNext()
        
        return result


    @staticmethod
    def Run(code):
        Parser.Toke=Tokenizer(code)
        result = Parser.Block()
        if(Parser.Toke.actual.type!="End"):
            raise TypeError("Finished Before EOF") 
        
        return result
