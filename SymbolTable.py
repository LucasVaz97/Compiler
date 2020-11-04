class Variable:
    def __init__(self,name,value,type_):
        self.name=name
        self.value=value
        self.type=type_


class SymbolTable:
    def __init__(self):
        self.table = {}

    def DeclareVariable(self,name,value,type_):
        variable=Variable(name,value,type_)
        if(variable.name not in self.table):
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

       

