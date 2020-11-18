from SymbolTable import *
from WriteAssembly import Compiler
symbT=SymbolTable()

pythonTypeDic={
    "str":"String",
    "int":"Int",
    "bool":"Bool",
    "NoneType":"None"
}

class Node:
    i=0
    def __init__(self,value,children):
        self.value=value
        self.children=children
        Node.i=Node.newId()
  

    def Evaluate(self):
        pass


    @staticmethod
    def newId():
        Node.i=Node.i+1
        return Node.i

class BinOp(Node):
    def __init__(self,value,children):
        self.binType=None
        super(BinOp, self).__init__(value, children)
    

    def GetType(self):
        return self.binType

    def Evaluate(self):
        if(self.value=="+"):
            if(self.children[0].GetType() != "String"):
                #result = self.children[0].Evaluate()+ self.children[1].Evaluate()
                self.children[0].Evaluate()
                Compiler.AddInstruction("PUSH EBX")
                self.children[1].Evaluate()
                Compiler.AddInstruction("POP EAX")
                Compiler.AddInstruction("ADD EAX,EBX")
                Compiler.AddInstruction("MOV EBX,EAX")
                self.binType="Int"
                #return result
            else:
                raise ValueError("Cannot Sum String")
        
        elif (self.value=="-"):
            #result = self.children[0].Evaluate()-self.children[1].Evaluate()
            self.children[0].Evaluate()
            Compiler.AddInstruction("PUSH EBX")
            self.children[1].Evaluate()
            Compiler.AddInstruction("POP EAX")
            Compiler.AddInstruction("SUB EAX, EBX")
            Compiler.AddInstruction("MOV EBX, EAX")
            self.binType="Int"

        elif (self.value=="*"):
            if(self.children[0].GetType() == "String" or self.children[1].GetType() == "String" ):
                result = str(self.children[0].Evaluate())+str(self.children[1].Evaluate())
            else:
                #result = self.children[0].Evaluate()*self.children[1].Evaluate()
                self.children[0].Evaluate()
                Compiler.AddInstruction("PUSH EBX")
                self.children[1].Evaluate()
                Compiler.AddInstruction("POP EAX")
                Compiler.AddInstruction("IMUL EBX")
                Compiler.AddInstruction("MOV EBX, EAX")
                self.binType="Int"

            

        elif (self.value=="/"):
            #result = self.children[0].Evaluate()/self.children[1].Evaluate()
            self.children[0].Evaluate()
            Compiler.AddInstruction("PUSH EBX")
            self.children[1].Evaluate()
            Compiler.AddInstruction("POP EAX")
            Compiler.AddInstruction("DIV EAX, EBX")
            Compiler.AddInstruction("MOV EBX, EAX")
            self.binType="Int"
            

        elif (self.value=="&&"):
            #result =  (self.children[0].Evaluate() and self.children[1].Evaluate())
            self.children[0].Evaluate()
            Compiler.AddInstruction("PUSH EBX")
            self.children[1].Evaluate()
            Compiler.AddInstruction("POP EAX")
            Compiler.AddInstruction("AND EAX, EBX")
            Compiler.AddInstruction("MOV EBX, EAX")
            self.binType="Bool"
           

        elif (self.value=="||"):
            #result =  (self.children[0].Evaluate() or self.children[1].Evaluate())
            self.children[0].Evaluate()
            Compiler.AddInstruction("PUSH EBX")
            self.children[1].Evaluate()
            Compiler.AddInstruction("POP EAX")
            Compiler.AddInstruction("OR EAX, EBX")
            Compiler.AddInstruction("MOV EBX, EAX")
            self.binType="Bool"

        elif (self.value=="=="):
            #result =  (self.children[0].Evaluate() == self.children[1].Evaluate())
            self.children[0].Evaluate()
            Compiler.AddInstruction("PUSH EBX")
            self.children[1].Evaluate()
            Compiler.AddInstruction("POP EAX")
            Compiler.AddInstruction("CMP EAX, EBX")
            Compiler.AddInstruction("CALL binop_je")
            self.binType="Bool"
        

        elif (self.value==">"):
            #result =  (self.children[0].Evaluate() > self.children[1].Evaluate())
            self.children[0].Evaluate()
            Compiler.AddInstruction("PUSH EBX")
            self.children[1].Evaluate()
            Compiler.AddInstruction("POP EAX")
            Compiler.AddInstruction("CMP EAX, EBX")
            Compiler.AddInstruction("CALL binop_jg")
            self.binType="Bool"

        elif (self.value=="<"):
            #result =  (self.children[0].Evaluate() < self.children[1].Evaluate())
            self.children[0].Evaluate()
            Compiler.AddInstruction("PUSH EBX")
            self.children[1].Evaluate()
            Compiler.AddInstruction("POP EAX")
            Compiler.AddInstruction("CMP EAX, EBX")
            Compiler.AddInstruction("CALL binop_jl")
            self.binType="Bool"


        else:
            raise ValueError("Invalid Operation")





class WhileOP(Node):
    def Evaluate(self):
        Compiler.AddInstruction("LOOP_{}:".format(Node.i))
        self.children[0].Evaluate()
        Compiler.AddInstruction("CMP EBX, False")
        Compiler.AddInstruction("JE EXIT_{}".format(Node.i))
        self.children[1].Evaluate()
        Compiler.AddInstruction("JMP LOOP_{}".format(Node.i))
        Compiler.AddInstruction("EXIT_{}:".format(Node.i))
      

class ifOP(Node):
    def Evaluate(self):
        self.children[0].Evaluate()
        Compiler.AddInstruction("CMP EBX, False")
        Compiler.AddInstruction("JE EXIT_{}".format(Node.i))
        self.children[1].Evaluate()
        Compiler.AddInstruction("EXIT_{}:".format(Node.i))
        if(len(self.children) and self.children[2]):
            self.children[0].Evaluate()
            Compiler.AddInstruction("CMP EBX, False")
            Compiler.AddInstruction("JNE EXIT_ELSE_{}".format(Node.i))
            self.children[2].Evaluate()
            Compiler.AddInstruction("EXIT_ELSE_{}:".format(Node.i))





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
        a=self.children[0].Evaluate()
        Compiler.AddInstruction("PUSH EBX")
        Compiler.AddInstruction("CALL print")
        Compiler.AddInstruction("POP EBX")



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
        Compiler.AddInstruction("MOV EBX, ",str(self.value))
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
        Compiler.AddInstruction("MOV EBX, [EBP-{}]".format(symbT.GetVariable(self.value).EBPNum))
        return symbT.GetVariable(self.value).value

    
class Varop(Node):

    def Evaluate(self):
        if(self.value=="="):
            Var=symbT.GetVariable(self.children[0].name)
            Var2=self.children[1].Evaluate()
            if(Var.type==self.children[1].GetType()):
                symbT.SetVariable(self.children[0].name,Var2)
                Compiler.AddInstruction("MOV [EBP-{}], EBX".format(Var.EBPNum))
            else:
                raise SyntaxError("Invalid Type association")
        else:
            raise ValueError("Invalid Operation")

class DeclareVal(Node):
    def Evaluate(self):
        Compiler.AddInstruction("PUSH DWORD 0")
        symbT.EBPNum+=4
        symbT.DeclareVariable(self.value,None,self.children[0])






class NoOp(Node):

    def Evaluate(self):
        pass
        

