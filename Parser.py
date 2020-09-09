from Tokenizer import Tokenizer

TypeDic={"+":"Plus",
        "-":"Minus",
        "*":"Multiply",
        "/":"Divide"}

class Parser:
    Toke=None
    @staticmethod
    def parseExpression():
        result=Parser.parseTerm()
        while(Parser.Toke.actual.type!="End"):
            if(Parser.Toke.actual.value in TypeDic):
                if(Parser.Toke.actual.type=="Plus"):
                    value=int(Parser.parseTerm())
                    result=result+value
                elif(Parser.Toke.actual.type=="Minus"):
                    value= int(Parser.parseTerm())
                    result=result-value
        return result

    @staticmethod
    def parseTerm():
        Parser.Toke.selectNext()
        if(Parser.Toke.actual.type=="Number"):
            result=int(Parser.Toke.actual.value)
            Parser.Toke.selectNext()

        else:raise TypeError("Not a Number")
  
        while(Parser.Toke.actual.type=="Multiply" or Parser.Toke.actual.type=="Divide"):
            if(Parser.Toke.actual.type=="Multiply"):
                Parser.Toke.selectNext()
                if(Parser.Toke.actual.type=="Number"):
                    value= int(Parser.Toke.actual.value)
                    result=result*value
                   
                else:
                    raise TypeError("Only integers are allowed")
            if(Parser.Toke.actual.type=="Divide"):
                Parser.Toke.selectNext()
                if(Parser.Toke.actual.type=="Number"):
                    value= int(Parser.Toke.actual.value)
                    result=int(result/value)
                else:
                    raise TypeError("Only integers are allowed") 


            Parser.Toke.selectNext()

        if(Parser.Toke.actual.type=="Number"):
            raise TypeError("Missing sign") 
        
        return result


    @staticmethod
    def run(code):
        Parser.Toke=Tokenizer(code)
        result = Parser.parseExpression()
        return result
