from SymbolTable import *
symbT=SymbolTable()

pythonTypeDic={
    "str":"String",
    "int":"Int",
    "bool":"Bool"
}

class Node:
    def __init__(self,value,children):
        self.value=value
        self.children=children

    def Evaluate(self):
        pass

class BinOp(Node):

    def Evaluate(self):
        if(self.value=="+"):
            if(self.children[0].GetType() != "String"):
                result = self.children[0].Evaluate()+ self.children[1].Evaluate()
                return result
            else:
                raise ValueError("Cannot Sum String")
        
        elif (self.value=="-"):
            result = self.children[0].Evaluate()-self.children[1].Evaluate()
            return result

        elif (self.value=="*"):
            if(self.children[0].GetType() == "String" or self.children[1].GetType() == "String" ):
                result = str(self.children[0].Evaluate())+str(self.children[1].Evaluate())
            else:
                result = self.children[0].Evaluate()*self.children[1].Evaluate()

            return result

        elif (self.value=="/"):
            result = self.children[0].Evaluate()/self.children[1].Evaluate()
            return int(result)

        elif (self.value=="&&"):
            result =  (self.children[0].Evaluate() and self.children[1].Evaluate())
            return bool(result)

        elif (self.value=="||"):
            result =  (self.children[0].Evaluate() or self.children[1].Evaluate())
            type_=type(result).__name__
            return bool(result)

        elif (self.value=="=="):
            result =  (self.children[0].Evaluate() == self.children[1].Evaluate())
            return bool(result)

        elif (self.value==">"):
            result =  (self.children[0].Evaluate() > self.children[1].Evaluate())
            return bool(result)

        elif (self.value=="<"):
            result =  (self.children[0].Evaluate() < self.children[1].Evaluate())
            return bool(result)


        else:
            raise ValueError("Invalid Operation")


    def GetType(self):
        type_=type(self.Evaluate()).__name__
        return pythonTypeDic[type_]



class WhileOP(Node):
    def Evaluate(self):
        while(self.children[0].Evaluate()):
            self.children[1].Evaluate()
      

class ifOP(Node):
    def Evaluate(self):
        if(self.children[0].GetType() == "String"):
            raise ValueError("Can not use String in if Statement")
        if(self.children[0].Evaluate()):
            self.children[1].Evaluate()
        else:
            if(self.children[2]!=None):
                self.children[2].Evaluate()
      


class UnOp(Node):

    def Evaluate(self):
        if(self.value=="+"):
            return self.children[0].Evaluate()

        if(self.value=="-"):
            return -self.children[0].Evaluate()

        if(self.value=="!"):
            return not self.children[0].Evaluate()

        if(self.value=="Variable"):
            return self.children[0].Evaluate()



class Block(Node):
    def Evaluate(self):
        for i in range(len(self.children)):
            self.children[i].Evaluate()


class Println(Node):
    def Evaluate(self):
        print(self.children[0].Evaluate())



class ReadLine(Node):
    def GetType(self):
        return "Int"

    def Evaluate(self):
        a= input()
        val=int(a)
        return val





class intVal(Node):
    def GetType(self):
        return "Int"

    def Evaluate(self):
        return int(self.value)

class StrVal(Node):

    def GetType(self):
        return "String"

    def Evaluate(self):
        return str(self.value)

class BoolVal(Node):

    def GetType(self):
        return "Bool"

    def Evaluate(self):
        return bool(self.value)


class Val(Node):
    def GetType(self):
        return symbT.GetVariable(self.value).type

    def Evaluate(self):
        return symbT.GetVariable(self.value).value

    



class Varop(Node):
    def Evaluate(self):
        if(self.value=="="):
            if(self.children[0].type==self.children[1].GetType()):
                symbT.SetVariable(self.children[0].name,self.children[1].Evaluate())
            else:
                raise SyntaxError("Invalid Type association")
                
        else:
            raise ValueError("Invalid Operation")





class NoOp(Node):

    def Evaluate(self):
        pass
        

