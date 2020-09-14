from Tokenizer import *

class Parser:
    Toke=None
    @staticmethod
    def parseExpression():
        result=Parser.parseTerm()
        while(Parser.Toke.actual.type=="Plus" or Parser.Toke.actual.type=="Minus"):
            if(Parser.Toke.actual.value in TypeDic):
                if(Parser.Toke.actual.type=="Plus"):
                    value=int(Parser.parseTerm())
                    result=result+value
                elif(Parser.Toke.actual.type=="Minus"):
                    value= int(Parser.parseTerm())
                    result=result+value
                elif(Parser.Toke.actual.type=="CloseP"):
                    Parser.Toke.selectNext()
                    return result

        return result

    @staticmethod
    def parseTerm():
        result=Parser.parseFactor(0)
        while(Parser.Toke.actual.type=="Multiply" or Parser.Toke.actual.type=="Divide"):
            if(Parser.Toke.actual.type=="Multiply"):
                Parser.Toke.selectNext()
                value=Parser.parseFactor(0)
                result = result*value
                print(Parser.Toke.actual.type)

            if(Parser.Toke.actual.type=="Divide"):
                Parser.Toke.selectNext()
                value=Parser.parseFactor(0)
                result = int(result/value)
                
        if(Parser.Toke.actual.type=="Number"):
            raise TypeError("Missing sign") 
    
        return result

    @staticmethod
    def parseFactor(counter):

        if(Parser.Toke.actual.type=="OpenP"):
            Parser.Toke.selectNext()
            result=Parser.parseExpression()
            if(Parser.Toke.actual.type=="CloseP"):
                Parser.Toke.selectNext()
                return(result)
            else:
                 raise TypeError("Missing Closed Parentesis") 
        elif(Parser.Toke.actual.type=="Plus"):
            Parser.Toke.selectNext()
            result=Parser.parseFactor(counter)
            return result
        elif(Parser.Toke.actual.type=="Minus"):
            Parser.Toke.selectNext()
            result=Parser.parseFactor(counter+1)
            return result
        elif(Parser.Toke.actual.type=="Number"):
            result=int(Parser.Toke.actual.value)
            Parser.Toke.selectNext()
            if(counter%2!=0):
                result=result*-1
            return result





    @staticmethod
    def run(code):
        Parser.Toke=Tokenizer(code)
        result = Parser.parseExpression()
        return result
