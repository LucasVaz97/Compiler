from Tokenizer import *
from Node import *

class Parser:
    Toke=None


    @staticmethod
    def Block():
        block=Block("Block",[])
        while(Parser.Toke.actual.type!="EOF" and Parser.Toke.actual.value!="end" and Parser.Toke.actual.value!="else" and Parser.Toke.actual.value!="elseif"):
            result=Parser.Command()
            block.children.append(result)
            Parser.Toke.selectNext()
        
           
        return block

    @staticmethod
    def Command():

        if(Parser.Toke.actual.type=="Reserved"):
            if(Parser.Toke.actual.value=="println"):
                Parser.Toke.selectNext()
                result=Parser.ParseRelExpression()
                printOb=Println("print",[])
                printOb.children.append(result)
                return printOb

            elif(Parser.Toke.actual.value=="if" or Parser.Toke.actual.value=="elseif"):
                ifOb=ifOP("if",[None,None,None])
                Parser.Toke.selectNext()
                rel=Parser.ParseRelExpression()
                ifOb.children[0]=(rel)
                

                if(Parser.Toke.actual.type=="NewLine"):
                    Parser.Toke.selectNext()
                    block=Parser.Block()
                    ifOb.children[1]=(block)

                    if(Parser.Toke.actual.value=="elseif"):
                        block2=Parser.Command()
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

        elif(Parser.Toke.actual.type=="Variable"):
            Variable=Parser.Toke.actual.value
            Parser.Toke.selectNext()
            result=Varop(Parser.Toke.actual.value,[Variable,None])
            Parser.Toke.selectNext()
            if(Parser.Toke.actual.value=="readline"):
                rl=ReadLine(None,[])
                result.children[1]=rl
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
                result.children[1]=Parser.ParseRelExpression()
            return result

    
            
        elif(Parser.Toke.actual.type!="NewLine"):
            raise TypeError("Insert Command ou Variable")

        
        return NoOp(0,[])



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
            result=Val(Parser.Toke.actual.value,None)
            Parser.Toke.selectNext()
        
        return result


    @staticmethod
    def Run(code):
        Parser.Toke=Tokenizer(code)
        result = Parser.Block()
        if(Parser.Toke.actual.type!="EOF" and Parser.Toke.actual.value!="end"):
            raise TypeError("Finished Before EOF") 
        
        result.Evaluate()
        return result
