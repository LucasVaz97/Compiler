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


class UnOp(Node):

    def Evaluate(self):
        if(self.value=="+"):
            return self.children[0].Evaluate()

        if(self.value=="-"):
            return -self.children[0].Evaluate()

        if(self.value=="Variable"):
            return self.children[0].Evaluate()


class intVal(Node):

    def Evaluate(self):
        return int(self.value)

class Val(Node):

    def Evaluate(self):
        return symbT.GetVariable(self.value)


class NoOp(Node):

    def Evaluate(self):
        pass



class SetEqual(Node):
    def Evaluate(self):
        symbT.SetVariable(self.children[0],self.children[1])


