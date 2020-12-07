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
    def Evaluate(self,symbT):
        if(self.value=="+"):
            if(self.children[0].__class__.__name__=="BinOp"):
                if(self.children[0].GetType(symbT) != "String"):
                    result = self.children[0].Evaluate(symbT)+ self.children[1].Evaluate(symbT)
                    return result
                else:
                    raise ValueError("Cannot Sum String")

            if(self.children[0].GetType(symbT) != "String"):
                result = self.children[0].Evaluate(symbT)+ self.children[1].Evaluate(symbT)
                return result
            else:
                raise ValueError("Cannot Sum String")
        
        elif (self.value=="-"):
            result = self.children[0].Evaluate(symbT)-self.children[1].Evaluate(symbT)
            return result

        elif (self.value=="*"):
            if(self.children[0].GetType(symbT) == "String" or self.children[1].GetType(symbT) == "String" ):
                result = str(self.children[0].Evaluate(symbT))+str(self.children[1].Evaluate(symbT))
            else:
                result = self.children[0].Evaluate(symbT)*self.children[1].Evaluate(symbT)

            return result

        elif (self.value=="/"):
            result = self.children[0].Evaluate(symbT)/self.children[1].Evaluate(symbT)
            return int(result)

        elif (self.value=="&&"):
            result =  (self.children[0].Evaluate(symbT) and self.children[1].Evaluate(symbT))
            return bool(result)

        elif (self.value=="||"):
            result =  (self.children[0].Evaluate(symbT) or self.children[1].Evaluate(symbT))
            type_=type(result).__name__
            return bool(result)

        elif (self.value=="=="):
            result =  (self.children[0].Evaluate(symbT) == self.children[1].Evaluate(symbT))
            return bool(result)

        elif (self.value==">"):
            result =  (self.children[0].Evaluate(symbT) > self.children[1].Evaluate(symbT))
            return bool(result)

        elif (self.value=="<"):
            result =  (self.children[0].Evaluate(symbT) < self.children[1].Evaluate(symbT))
            return bool(result)


        else:
            raise ValueError("Invalid Operation")


    def GetType(self,symbT):
        type_=type(self.Evaluate(symbT)).__name__
        return pythonTypeDic[type_]



class WhileOP(Node):
    def Evaluate(self,symbT):
        while(self.children[0].Evaluate(symbT)):
            self.children[1].Evaluate(symbT)
      

class ifOP(Node):
    def Evaluate(self,symbT):
        if(self.children[0].GetType(symbT) == "String"):
            raise ValueError("Can not use String in if Statement")
        if(self.children[0].Evaluate(symbT)):
            self.children[1].Evaluate(symbT)
        else:
            if(self.children[2]!=None):
                self.children[2].Evaluate(symbT)
      


class UnOp(Node):

    def Evaluate(self,symbT):
        if(self.value=="+"):
            return self.children[0].Evaluate(symbT)

        if(self.value=="-"):
            return -self.children[0].Evaluate(symbT)

        if(self.value=="!"):
            return not self.children[0].Evaluate(symbT)

        if(self.value=="Variable"):
            return self.children[0].Evaluate(symbT)

    def GetType(self,symbT):
        return self.children[0].GetType(symbT)




class Block(Node):
    def Evaluate(self,symbT):
        for i in range(len(self.children)):
            if(symbT.table["Return"].value==None):
                self.children[i].Evaluate(symbT)
            else:
                break





class Println(Node):
    def Evaluate(self,symbT):
        print(self.children[0].Evaluate(symbT))

class ReadLine(Node):
    def GetType(self,symbT):
        return "Int"

    def Evaluate(self,symbT):
        a= input()
        val=int(a)
        return val

class intVal(Node):
    def GetType(self,symbT):
        return "Int"

    def Evaluate(self,symbT):
        return int(self.value)

class StrVal(Node):

    def GetType(self,symbT):
        return "String"

    def Evaluate(self,symbT):
        return str(self.value)

class BoolVal(Node):

    def GetType(self,symbT):
        return "Bool"

    def Evaluate(self,symbT):
        return bool(self.value)


class Val(Node):
    def GetType(self,symbT):
        return symbT.GetVariable(self.value).type

    def Evaluate(self,symbT):
        if(symbT.GetVariable(self.value).value !=  None):
            return symbT.GetVariable(self.value).value
        else:
            raise ValueError("No value associated to variable: {}".format(self.value))


class Varop(Node):
    def Evaluate(self,symbT):
        variable=symbT.GetVariable(self.value)
        if(self.children[1]=="="):
            if(self.children[0].__class__.__name__=="BinOp" or self.children[0].__class__.__name__=="FuncReturn"):
                if(variable.type==self.children[0].GetType(symbT)):
                    symbT.SetVariable(variable.name,self.children[0].Evaluate(symbT))
                else:
                    raise SyntaxError("Invalid Type association")
            else:
                if(variable.type==self.children[0].GetType(symbT)):
                    symbT.SetVariable(variable.name,self.children[0].Evaluate(symbT))
                else:
                    raise SyntaxError("Invalid Type association")
         
        else:
            raise ValueError("Invalid Operation")


class DeclareVar(Node):
    def __init__(self,value,children,type_):
        super().__init__(value,children)
        self.type_=type_

    def Evaluate(self,symbT):
        symbT.DeclareVariable(self.value,None,self.type_)


class NoOp(Node):

    def Evaluate(self,symbT):
        pass

class DeclareFunc(Node):
    def __init__(self,value,children,type_):
        super().__init__(value,children)
        self.type=type_

    def Evaluate(self,symbT):
        symbT.DeclareFunction(self)


class FuncReturn(Node):
    def Evaluate(self,symbT):
        callSimb=SymbolTable()
        compareFunc=symbT.functable[self.value]
        if(self.value == compareFunc.value):
            if(len(self.children) == len(compareFunc.children)-1):
                for i in range(len(self.children)):
                    typeN=None
                    className=self.children[i].__class__.__name__
                    if(className=="BinOp"):
                        typeN=self.children[i].GetType(symbT)
                    else:
                        typeN=self.children[i].GetType(symbT)

                    if(typeN==compareFunc.children[i].type):
                        value=(self.children[i].Evaluate(symbT))
                        name=compareFunc.children[i].name
                        Var=Variable(name,value,typeN)
                        callSimb.table[compareFunc.children[i].name]=Var
                    else:
                        raise ValueError("Expected different type of arguments in function call")
            else:
                raise ValueError("Expected different number of arguments in function call")
        
        compareFunc.children[-1].Evaluate(callSimb)

        if(callSimb.table["Return"].type==compareFunc.type):
            return callSimb.table["Return"].value
        else:
            raise ValueError("Invalid return type for return function")

    def GetType(self,symbT):
        return symbT.functable[self.value].type



        
class ReturnNode(Node):
    def Evaluate(self,symbT):
        value=self.children[0].Evaluate(symbT)
        symbT.table["Return"].value=value
        typeN=None

        className=self.children[0].__class__.__name__
        if(className=="BinOp"):
            typeN=self.children[0].GetType(symbT)
        else:
            typeN=self.children[0].GetType(symbT)

        symbT.table["Return"].type=typeN

        


        


        

        

        



        

