import sys
from Lexer import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.simbolos = set()    
        self.etiquetasdeclarada = set() 
        self.etiquetasGotoed = set() 

        self.tokenActual = None
        self.tokenObservandose = None
        self.siguienteToken()
        self.siguienteToken()    

    
    def revisarToken(self, kind):
        return kind == self.tokenActual.kind

    
    def analizarToken(self, kind):
        return kind == self.tokenObservandose.kind

    
    def comparaToken(self, kind):
        if not self.revisarToken(kind):
            self.Abortar("Esperando " + kind.name + ", encontro " + self.tokenActual.kind.name)
        self.siguienteToken()

    
    def siguienteToken(self):
        self.tokenActual = self.tokenObservandose
        self.tokenObservandose = self.lexer.omitirToken()
        

    
    def revisaOperadorComparacion(self):
        return self.revisarToken(tipoToken.MAYOR) or self.revisarToken(tipoToken.MAYORIGUAL) or self.revisarToken(tipoToken.MENORQUE) or self.revisarToken(tipoToken.MENORIGUAL) or self.revisarToken(tipoToken.IGUAL) or self.revisarToken(tipoToken.DISTINTOA)

    def Abortar(self, message):
        sys.exit("Error. " + message)


    

    
    def programa(self):
        print("programa")

       
        while self.revisarToken(tipoToken.NUEVA_LINEA):
            self.siguienteToken()

        
        while not self.revisarToken(tipoToken.FIN_DE_LINEA):
            self.declaracion()

        
        for etiqueta in self.etiquetasGotoed:
            if etiqueta not in self.etiquetasdeclarada:
                self.Abortar("intentando ir a una etiqueta no declarada: " + etiqueta)


    
    def declaracion(self):
        

        
        if self.revisarToken(tipoToken.IMPRIMIR):
            print("Imprimiendo declaración")
            self.siguienteToken()

            if self.revisarToken(tipoToken.STRING):
               
                self.siguienteToken()

            else:
               
                self.expresion()

       
        elif self.revisarToken(tipoToken.IF):
            print("declarando IF")
            self.siguienteToken()
            self.comparacionn()

            self.comparaToken(tipoToken.THEN)
            self.nl()

           
            while not self.revisarToken(tipoToken.ENDIF):
                self.declaracion()

            self.comparaToken(tipoToken.ENDIF)

        
        elif self.revisarToken(tipoToken.WHILE):
            print("declarando WHILE")
            self.siguienteToken()
            self.comparacionn()

            self.comparaToken(tipoToken.REPETIR)
            self.nl()

           
            while not self.revisarToken(tipoToken.ENDWHILE):
                self.declaracion()

            self.comparaToken(tipoToken.ENDWHILE)

        elif self.revisarToken(tipoToken.LABEL):
            print("declarando etiqueta")
            self.siguienteToken()

            
            if self.tokenActual.text in self.etiquetasdeclarada:
                self.Abortar("etiqueta ya existente: " + self.tokenActual.text)
            self.etiquetasdeclarada.add(self.tokenActual.text)

            self.comparaToken(tipoToken.VARIABLE)

        
        elif self.revisarToken(tipoToken.GOTO):
            print("declaracion-GOTO")
            self.siguienteToken()
            self.etiquetasGotoed.add(self.tokenActual.text)
            self.comparaToken(tipoToken.VARIABLE)

        
        elif self.revisarToken(tipoToken.INT):
            print("declaracion-INT")
            self.siguienteToken()

           
            if self.tokenActual.text not in self.simbolos:
                self.simbolos.add(self.tokenActual.text)

            self.comparaToken(tipoToken.VARIABLE)
            self.comparaToken(tipoToken.IGUAL)
            
            self.expresion()

        
        elif self.revisarToken(tipoToken.ENTRADA):
            print("declaracion-Entrada")
            self.siguienteToken()

            
            if self.tokenActual.text not in self.simbolos:
                self.simbolos.add(self.tokenActual.text)

            self.comparaToken(tipoToken.VARIABLE)

        
        else:
            self.Abortar("declaracion invalida " + self.tokenActual.text + " (" + self.tokenActual.kind.name + ")")

        
        self.nl()


    
    def comparacionn(self):
        print("comparacion")

        self.expresion()
        
        if self.revisaOperadorComparacion():
            self.siguienteToken()
            self.expresion()
        else:
            self.Abortar("Operador de comparación esperado en: " + self.tokenActual.text)

       
        while self.revisaOperadorComparacion():
            self.siguienteToken()
            self.expresion()


    
    def expresion(self):
        print("expresion")

        self.terminoMat()
        
        while self.revisarToken(tipoToken.SUMA) or self.revisarToken(tipoToken.RESTA):
            self.siguienteToken()
            self.terminoMat()


    
    def terminoMat(self):
        print("terminoMat")

        self.unario()
        
        while self.revisarToken(tipoToken.ASTERISCO) or self.revisarToken(tipoToken.DIAGONAL):
            self.siguienteToken()
            self.unario()


    
    def unario(self):
        print("unario")
        
        if self.revisarToken(tipoToken.SUMA) or self.revisarToken(tipoToken.RESTA):
            self.siguienteToken()        
        self.primario()


    
    def primario(self):
        print("primario (" + self.tokenActual.text + ")")

        if self.revisarToken(tipoToken.NUMERO): 
            self.siguienteToken()
        elif self.revisarToken(tipoToken.VARIABLE):
            
            if self.tokenActual.text not in self.simbolos:
                self.Abortar("Variable de referencia antes de la asignación: " + self.tokenActual.text)

            self.siguienteToken()
        else:
            
            self.Abortar("Token inesperado en " + self.tokenActual.text)

    
    def nl(self):
        print("Nueva Linea")

        
        self.comparaToken(tipoToken.NUEVA_LINEA)
        
        while self.revisarToken(tipoToken.NUEVA_LINEA):
            self.siguienteToken()