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
        "&&":"And",
        "||":"Or",
        "==":"EqualCompare",
        "::":"Declaration"
}





Reserved={"println":"Reserved",
          "end":"Reserved",
          "while":"Reserved",
          "readline":"Reserved",
          "if":"Reserved",
          "else":"Reserved",
          "elseif":"Reserved",
          "local":"Scope",
          "Int":"Type",
          "Bool":"Type",
          "String":"Type",
          "true":"Bool",
          "false":"Bool"
}


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
       
        elif(self.origin[self.position] in digits):
            num=""
            while(self.position!=len(self.origin) and self.origin[self.position] in digits):
                num=num+self.origin[self.position]
                self.position+=1
            self.actual=Token("Number",num)

        elif(self.origin[self.position] not in digits and not self.origin[self.position].isalpha()) and self.origin[self.position]!='"' :
            simbol=""
            single=self.origin[self.position]
        
            while(self.position!=len(self.origin) and self.origin[self.position] not in digits and not self.origin[self.position].isalpha() and self.origin[self.position]!="\n" and " " not in self.origin[self.position]):
                simbol=simbol+self.origin[self.position]
                self.position+=1
                if(simbol in TypeDic):
                    if(self.position!=len(self.origin)):
                        double=simbol+self.origin[self.position]
                        if(double in TypeDic):
                            self.actual=Token(TypeDic[double],double)
                            self.position+=1
                        else:
                            self.actual=Token(TypeDic[simbol],simbol)
                    
                        return

            self.actual=Token(TypeDic[simbol],simbol)


        elif(self.origin[self.position]=='"'):
            string=''
            self.position+=1
            while(self.origin[self.position]!='"'):
                string+=self.origin[self.position]
                self.position+=1
                if(self.position==len(self.origin)):
                    raise Exception ('Missing " ')
            
            self.position+=1
            self.actual=Token("String",string)
            

        else:
            var=""
            condition=True
            while(self.position!=len(self.origin) and self.origin[self.position] not in TypeDic and (self.origin[self.position].isalnum() or self.origin[self.position]=="_") and self.origin[self.position]!="\n" and " " not in self.origin[self.position]):
                var=var+self.origin[self.position]
                self.position+=1

            if(var in Reserved):
                self.actual=Token(Reserved[var],var)
            else:
                var=var.replace(" ","")
                self.actual=Token("Variable",var)
