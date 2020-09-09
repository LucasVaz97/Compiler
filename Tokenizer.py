import re

TypeDic={"+":"Plus",
        "-":"Minus",
        "*":"Multiply",
        "/":"Divide"}


class Token:
    def __init__(self, type_,value):
        self.type = type_
        self.value = value


class Tokenizer:
    def __init__(self,origin):
        self.origin = origin
        self.origin=re.sub("(#=)((.|\n)*?)(=#)","",origin)
        self.position = 0
        self.actual=""

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