class Variable:
    def __init__(self,name,value,type_):
        self.name=name
        self.value=value
        self.type=type_

class SymbolTable:
    functable={}

    def __init__(self):
        self.table = {"Return":Variable("Return",None,None)}

    def DeclareVariable(self,name,value,type_):
        variable=Variable(name,value,type_)
        if(variable.name not in self.table and variable.name not in SymbolTable.functable):
            self.table[variable.name]=variable
        else:
            raise ValueError(f"Variable: {variable.name} is already declared")

    def GetVariable(self,variable):
        if(variable in self.table):
            return self.table[variable]
        else:
            raise ValueError(f"Variable: {variable} is not declared")


    def SetVariable(self,variable,value):
        if(variable in self.table):
            self.table[variable].value=value
        else:
            raise ValueError(f"Variable: {variable} is not declared")


    def DeclareFunction(self,node):
        if(node.value not in SymbolTable.functable and node.value not in self.table):
            SymbolTable.functable[node.value]=node
        else:
            raise ValueError(f"Funcion: {name} is already declared")

    
    def GetFunction(self,funcName):
        if(funcName in self.table):
            return self.table[funcName]
        else:
            raise ValueError(f"Function: {funcName} is not declared")

    



       

