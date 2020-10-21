import re

TypeDic={"+":"Plus",
        "-":"Minus",
        "*":"Multiply",
        "/":"Divide",
        "(":"OpenP",
        ")":"CloseP",
        "=":"Equal",
        "!":"Not",
        ">":"Bigger",
        "<":"Smaller",
        "&":"And",
        "|":"Or"}

DoublesDic={
        "&&":"And",
        "||":"Or",
        "==":"EqualCompare",
}

KeyWords=["println","end","while","readline","if","else","elseif"]


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
        self.selectNext()

    def selectNext(self):
        digits="0123456789"
        if(self.position==len(self.origin)):
            self.actual=Token("EOF",0)
        elif(self.origin[self.position] in " \f"):
            self.position+=1
            self.selectNext()
        elif(self.origin[self.position]=="\n"):
            self.actual=Token("NewLine",0)
            self.position+=1
        elif(self.origin[self.position] not in digits and self.origin[self.position] in TypeDic):
            self.actual=Token(TypeDic[self.origin[self.position]],self.origin[self.position])
            if(self.position+1<len(self.origin)):
                double=self.origin[self.position]+self.origin[self.position+1]
                if(double in DoublesDic):
                    self.actual=Token(DoublesDic[double],double)
                    self.position+=1
        
            self.position+=1
        elif(self.origin[self.position] in digits):
            num=""
            while(self.position!=len(self.origin) and self.origin[self.position] in digits):
                num=num+self.origin[self.position]
                self.position+=1
            self.actual=Token("Number",num)
        else:
            var=""
            condition=True
            while(self.position!=len(self.origin) and self.origin[self.position] not in TypeDic and self.origin[self.position].isalpha and self.origin[self.position]!="\n"):
                if(self.origin[self.position]==" "):
                    self.position+=1
                    break
                var=var+self.origin[self.position]
                self.position+=1

            if(var in KeyWords):
                self.actual=Token("Reserved",var)
            else:
                var=var.replace(" ","")
                self.actual=Token("Variable",var)
