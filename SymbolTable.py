class SymbolTable:
    def __init__(self):
        self.table = {}

    def DeclareVariable(self,variable,type):
        if(variable not in self.table):
            self.table[variable]=type
        else:
            raise ValueError(f"Variable: {variable} is already declared")


    def GetVariable(self,variable):
        return self.table[variable]


    def SetVariable(self,variable,type):
        self.table[variable]=type
       
