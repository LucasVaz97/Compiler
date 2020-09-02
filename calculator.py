import sys
#print('Argument List:', str(sys.argv))

TypeDic={"+":"Plus",
        "-":"Minus"}



class Token:
    def __init__(self, type_,value):
        self.type = type_
        self.value = value


class Tokenizer:
    def __init__(self,origin):
        self.origin = origin
        self.position = 0
        self.actual=""
        self.selectNext()
    
    def selectNext(self):
        digits="0123456789"
        if(self.position==len(self.origin)):
            self.actual=Token("End",0)
        elif(self.origin[self.position] in " \f"):
            self.position+=1
            self.selectNext()
        elif(self.origin[self.position] not in digits):
            self.actual=Token(TypeDic[self.origin[self.position]],self.origin[self.position])
            self.position+=1
        else:
            num=""
            while(self.position!=len(self.origin) and self.origin[self.position] in digits):
                num=num+self.origin[self.position]
                self.position+=1
            self.actual=Token("Number",num)

class Parser:
    Toke=None
    @staticmethod
    def parseExpression():
        result=0
        if(Parser.Toke.actual.value not in TypeDic):
            result=int(Parser.Toke.actual.value)
            Parser.Toke.selectNext()

        else:
            raise TypeError("Invalid Sintax")

        while(Parser.Toke.actual.type!="End"):
            if(Parser.Toke.actual.value in TypeDic):
                if(Parser.Toke.actual.type=="Plus"):
                    Parser.Toke.selectNext()
                    if(Parser.Toke.actual.type=="Number"):
                        value= int(Parser.Toke.actual.value)
                        result=result+value
                        Parser.Toke.selectNext()
                    else:
                        raise TypeError("Only integers are allowed")
                if(Parser.Toke.actual.type=="Minus"):
                    Parser.Toke.selectNext()
                    if(Parser.Toke.actual.type=="Number"):
                        value= int(Parser.Toke.actual.value)
                        result=result-value
                        Parser.Toke.selectNext()
                    else:
                        raise TypeError("Only integers are allowed")

            if(Parser.Toke.actual.type=="Number"):
                if(Parser.Toke.actual.type=="Number"):
                     raise TypeError("Invalid Sintax")
                else:  
                    Parser.Toke.selectNext()

            
                    

        return (result)
     

    @staticmethod
    def run(code):
        Parser.Toke=Tokenizer(code)
        result = Parser.parseExpression()
        return result



def main():
    code=sys.argv[1]
    result = Parser.run(code)

    return result

main()












