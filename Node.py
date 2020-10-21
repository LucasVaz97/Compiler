from SymbolTable import *
symbT=SymbolTable()

class Node:
    def __init__(self,value,children):
        self.value=value
        self.children=children

    def Evaluate(self):
        pass

class BinOp(Node):
    
    def Evaluate(self):
        if(self.value=="+"):
            result = self.children[0].Evaluate()+self.children[1].Evaluate()
            return result
        
        elif (self.value=="-"):
            result = self.children[0].Evaluate()-self.children[1].Evaluate()
            return result

        elif (self.value=="*"):
            result = self.children[0].Evaluate()*self.children[1].Evaluate()
            return result

        elif (self.value=="/"):
            result = self.children[0].Evaluate()/self.children[1].Evaluate()
            return int(result)

        elif (self.value=="&&"):
            result =  (self.children[0].Evaluate() and self.children[1].Evaluate())
            return (result)

        elif (self.value=="||"):
            result =  (self.children[0].Evaluate() or self.children[1].Evaluate())
            return (result)

        elif (self.value=="=="):
            result =  (self.children[0].Evaluate() == self.children[1].Evaluate())
            return (result)

        elif (self.value==">"):
            result =  (self.children[0].Evaluate() > self.children[1].Evaluate())
            return (result)

        elif (self.value=="<"):
            result =  (self.children[0].Evaluate() < self.children[1].Evaluate())
            return (result)


        else:
            raise ValueError("Invalid Operation")



class WhileOP(Node):
    def Evaluate(self):
        while(self.children[0].Evaluate()):
            self.children[1].Evaluate()
      

class ifOP(Node):
    def Evaluate(self):
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
    def Evaluate(self):
        a= input()
        val=int(a)
        return val





class intVal(Node):

    def Evaluate(self):
        return int(self.value)


class Val(Node):

    def Evaluate(self):
        return symbT.GetVariable(self.value)


class Varop(Node):
    def Evaluate(self):
        if(self.value=="="):
            symbT.SetVariable(self.children[0],self.children[1].Evaluate())
        else:
            raise ValueError("Invalid Operation")





class NoOp(Node):

    def Evaluate(self):
        pass
        


