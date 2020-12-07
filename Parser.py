from Tokenizer import *
from Node import *
from SymbolTable import *

class Parser:
    Toke=None

    @staticmethod
    def Block():
        block=Block("Block",[])
        while(Parser.Toke.actual.type!="EOF" and Parser.Toke.actual.value!="end" and Parser.Toke.actual.value!="else" and Parser.Toke.actual.value!="elseif"):
            result=Parser.Command()
            if(result!=None):
                block.children.append(result)
            Parser.Toke.selectNext()
        
        return block

    @staticmethod
    def BlockMain():
        block=Block("Block",[])
        result=None
        while(Parser.Toke.actual.type!="EOF"):
            if(Parser.Toke.actual.value=="function"):
                Parser.Toke.selectNext()
                if(Parser.Toke.actual.type=="Variable"):
                    FuncDecObj=DeclareFunc(Parser.Toke.actual.value,[],None)
                    Parser.Toke.selectNext()
                    if(Parser.Toke.actual.type=="OpenP"):
                        NoArgument=True
                        while((Parser.Toke.actual.value=="," or Parser.Toke.actual.type=="OpenP") and NoArgument):
                            Parser.Toke.selectNext()
                            if(Parser.Toke.actual.type=="CloseP"):
                                break
                            varName=None
                            type_=None
                            if(Parser.Toke.actual.type=="Variable"):
                                varName=Parser.Toke.actual.value
                                Parser.Toke.selectNext()
                                if(Parser.Toke.actual.type=="Declaration"):
                                    Parser.Toke.selectNext()
                                    if(Parser.Toke.actual.type=="Type"):
                                        type_=Parser.Toke.actual.value
                                        Parser.Toke.selectNext()
                                        valObj=Variable(varName,None,type_)
                                        FuncDecObj.children.append(valObj)
                                    else:
                                        raise SyntaxError("Invalid Type declaration")
                                else:
                                    raise SyntaxError("Missing declaration :: after Variable")

                            else:
                                raise SyntaxError("Declaration is not a variable")
                        
                        if(Parser.Toke.actual.type!="CloseP"):
                            raise SyntaxError("Missing Closed Parentesis")
                    else:
                        raise SyntaxError("Missing Open Parentesis")

                    Parser.Toke.selectNext()
                    if(Parser.Toke.actual.type=="Declaration"):
                        Parser.Toke.selectNext()
                        if(Parser.Toke.actual.type=="Type"):
                            FuncDecObj.type=Parser.Toke.actual.value
                            Parser.Toke.selectNext()
                            blockFunc=Parser.Block()
                            FuncDecObj.children.append(blockFunc)
                            if(Parser.Toke.actual.value != "end"):
                                raise SyntaxError("Missind end at function declaration")
                        else:
                            raise SyntaxError("Missing return Type for function")
                    else:
                        raise SyntaxError("Missing return Type '::' after function Declaration")


                    #Parser.Toke.selectNext()
                    result = FuncDecObj


            else:
                result=Parser.Command()
            if(result!=None):
                block.children.append(result)
            
            Parser.Toke.selectNext()
        return block



    @staticmethod
    def Command(elseif=False):
    
        if(Parser.Toke.actual.type=="Reserved"):

            if(Parser.Toke.actual.value=="return"):
                Parser.Toke.selectNext()
                result = ReturnNode(None,[])
                result.children.append(Parser.ParseRelExpression())
                return result

            elif(Parser.Toke.actual.value=="println"):
                Parser.Toke.selectNext()
                if(Parser.Toke.actual.type=="OpenP"):
                    Parser.Toke.selectNext()
                    result=Parser.ParseRelExpression()
                    printOb=Println("print",[])
                    printOb.children.append(result)
                    if(Parser.Toke.actual.type=="CloseP"):
                        Parser.Toke.selectNext()
                        return printOb
                    else:
                        raise SyntaxError("Missing Close Parentesis")

                else:
                    raise SyntaxError("Missing Open Parentesis")

            elif(Parser.Toke.actual.value=="if" or elseif):
                ifOb=ifOP("if",[None,None,None])
                Parser.Toke.selectNext()
                rel=Parser.ParseRelExpression()
                ifOb.children[0]=(rel)
                

                if(Parser.Toke.actual.type=="NewLine"):
                    Parser.Toke.selectNext()
                    block=Parser.Block()
                    ifOb.children[1]=(block)

                    if(Parser.Toke.actual.value=="elseif"):
                        block2=Parser.Command(True)
                        ifOb.children[2]=(block2)

                    elif(Parser.Toke.actual.value=="else"):
                        Parser.Toke.selectNext()
                        block2=Parser.Block()
                        ifOb.children[2]=(block2)

                if(Parser.Toke.actual.value!="end"):
                    raise ValueError("Missing end")
     
                return ifOb

            elif(Parser.Toke.actual.value=="while"):
                whileOb=WhileOP("while",[])
                Parser.Toke.selectNext()
                rel=Parser.ParseRelExpression()
                whileOb.children.append(rel)
                if(Parser.Toke.actual.type=="NewLine"):
                    Parser.Toke.selectNext()
                    block=Parser.Block()
                    whileOb.children.append(block)

                    if(Parser.Toke.actual.value!="end"):
                        raise ValueError("Missing end")
                    return whileOb
                    
                else:
                    raise ValueError("Invalid Sintax")    

            else:
                raise SyntaxError("Invalid Sintax")

        elif(Parser.Toke.actual.type=="Scope"):
            Parser.Toke.selectNext()
            if(Parser.Toke.actual.type=="Variable"):
                var=Parser.Toke.actual.value
                Parser.Toke.selectNext()
                if(Parser.Toke.actual.type=="Declaration"):
                    Parser.Toke.selectNext()
                    if(Parser.Toke.actual.type=="Type"):
                        type_=Parser.Toke.actual.value
                        delareOb=DeclareVar(var,[],type_)
                        Parser.Toke.selectNext()
                        return delareOb
                    else:
                        raise ValueError("Missing var type declaration")
                else:
                    raise ValueError("Missing Declaration after variable --> :: ")
            else:
                raise ValueError("Missing Variable after Scope")
            
        elif(Parser.Toke.actual.type=="Variable"):
            Var=Parser.Toke.actual.value
            back=None
            Parser.Toke.selectNext()
            if(Parser.Toke.actual.type=="OpenP"):
                result=FuncReturn(Var,[])
                Parser.Toke.selectNext()
                if(Parser.Toke.actual.type!="CloseP"):
                    result.children.append(Parser.ParseRelExpression())
                    while(Parser.Toke.actual.value==","):
                        Parser.Toke.selectNext()
                        result.children.append(Parser.ParseRelExpression())        
              
                if(Parser.Toke.actual.type!="CloseP"):
                    raise SyntaxError("Missing closed Parentesis")

                Parser.Toke.selectNext() 
                return result
            else:
                result=Varop(Var,[None,Parser.Toke.actual.value])
                Parser.Toke.selectNext()
            if(Parser.Toke.actual.value=="readline"):
                rl=ReadLine(None,[])
                result.children[0]=rl
                Parser.Toke.selectNext()
                if(Parser.Toke.actual.type=="OpenP"):
                    Parser.Toke.selectNext()
                    if(Parser.Toke.actual.type=="CloseP"):
                        Parser.Toke.selectNext()
                    else:
                        raise ValueError("Missing Closed Parentesis")
                else:
                     raise ValueError("Missing Parentesis")
            else:
                result.children[0]=Parser.ParseRelExpression()
            return result
   
            
        elif(Parser.Toke.actual.type!="NewLine"):
            raise TypeError("Insert Command ou Variable")

        return None

    @staticmethod
    def ParseRelExpression():
        result=Parser.ParseExpression()
        while(Parser.Toke.actual.type=="Bigger" or Parser.Toke.actual.type=="Smaller" or Parser.Toke.actual.type=="EqualCompare"):
            result=BinOp(Parser.Toke.actual.value,[result,None])
            Parser.Toke.selectNext()
            result.children[1]=Parser.ParseTerm()
        return result

    @staticmethod
    def ParseExpression():
        result=Parser.ParseTerm()
        while(Parser.Toke.actual.type=="Plus" or Parser.Toke.actual.type=="Minus" or Parser.Toke.actual.type=="Or"):
            result=BinOp(Parser.Toke.actual.value,[result,None])
            Parser.Toke.selectNext()
            result.children[1]=Parser.ParseTerm()
        return result

    @staticmethod
    def ParseTerm():
        result=Parser.ParseFactor()
        while(Parser.Toke.actual.type=="Multiply" or Parser.Toke.actual.type=="Divide" or Parser.Toke.actual.type=="And"):
            result=BinOp(Parser.Toke.actual.value,[result,None])
            Parser.Toke.selectNext()
            result.children[1]=Parser.ParseFactor()
          
        if(Parser.Toke.actual.type=="Number"):
            raise TypeError("Missing sign") 

        if(Parser.Toke.actual.type=="String"):
            raise TypeError("Cannot declare 'String' 'String'") 
    
        return result

    @staticmethod
    def ParseFactor():
        result=0
        if(Parser.Toke.actual.type=="OpenP"):
            Parser.Toke.selectNext()
            result=Parser.ParseRelExpression()
            if(Parser.Toke.actual.type=="CloseP"):
                Parser.Toke.selectNext()
                return(result)
            else:
                 raise TypeError("Missing Closed Parentesis") 

        elif(Parser.Toke.actual.type=="Plus" or Parser.Toke.actual.type=="Minus"or Parser.Toke.actual.type=="Not"):
            result=UnOp(Parser.Toke.actual.value,[result])
            Parser.Toke.selectNext()
            result.children[0]=Parser.ParseFactor()

        elif(Parser.Toke.actual.type=="Number"):
            result=intVal(Parser.Toke.actual.value,None)
            Parser.Toke.selectNext()

        elif(Parser.Toke.actual.type=="Variable"):
            Var=Parser.Toke.actual.value
            Parser.Toke.selectNext()
            if(Parser.Toke.actual.type=="OpenP"):
                result=FuncReturn(Var,[])
                Parser.Toke.selectNext()
                if(Parser.Toke.actual.type!="CloseP"):
                    result.children.append(Parser.ParseRelExpression())
                    while(Parser.Toke.actual.value==","):
                        Parser.Toke.selectNext()
                        result.children.append(Parser.ParseRelExpression()) 
                       

                if(Parser.Toke.actual.type!="CloseP"):
                    raise SyntaxError("Missing closed Parentesis")
                else:
                    Parser.Toke.selectNext()

            else:
                result=Val(Var,None)

            

        elif(Parser.Toke.actual.type=="String"):
            result=StrVal(Parser.Toke.actual.value,None)
            Parser.Toke.selectNext()

        elif(Parser.Toke.actual.type=="Bool"):
            condition=None
            if(Parser.Toke.actual.value=="true"):
                condition=True
            else:
                condition=False
            result=BoolVal(condition,None)
            Parser.Toke.selectNext()
        
        else:
            raise TypeError("Invalid Operation")

        return result


    @staticmethod
    def Run(code):
        Parser.Toke=Tokenizer(code)
        result = Parser.BlockMain()
        if(Parser.Toke.actual.type!="EOF" and Parser.Toke.actual.value!="end"):
            raise TypeError("Finished Before EOF") 
        
        result.Evaluate(symbT)
        return result
