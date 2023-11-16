import enum
import sys

class Lexer:
    def __init__(self, entrada):
        self.codigo = entrada + '\n' 
        self.caracterActual = ''   
        self.posicionActual = -1    
        self.siguienteCaracter()

    
    def siguienteCaracter(self):
        self.posicionActual += 1
        if self.posicionActual >= len(self.codigo):
            self.caracterActual = '\0'  
        else:
            self.caracterActual = self.codigo[self.posicionActual]

    
    def peek(self):
        if self.posicionActual + 1 >= len(self.codigo):
            return '\0'
        return self.codigo[self.posicionActual+1]

    
    def Abortar(self, message):
        sys.exit("Error Lexico. " + message)
		
    
    def omitirEspacioBlanco(self):
        while self.caracterActual == ' ' or self.caracterActual == '\t' or self.caracterActual == '\r':
            self.siguienteCaracter()
		
    
    def omitirComentario(self):
        if self.caracterActual == '#':
            while self.caracterActual != '\n':
                self.siguienteCaracter()

   
    def omitirToken(self):
        self.omitirEspacioBlanco()
        self.omitirComentario()
        token = None

        
        if self.caracterActual == '+':
            token = Token(self.caracterActual, tipoToken.SUMA)
        elif self.caracterActual == '-':
            token = Token(self.caracterActual, tipoToken.RESTA)
        elif self.caracterActual == '*':
            token = Token(self.caracterActual, tipoToken.ASTERISCO)
        elif self.caracterActual == '/':
            token = Token(self.caracterActual, tipoToken.DIAGONAL)
        elif self.caracterActual == '=':
            
            if self.peek() == '=':
                lastChar = self.caracterActual
                self.siguienteCaracter()
                token = Token(lastChar + self.caracterActual, tipoToken.IGUALIGUAL)
            else:
                token = Token(self.caracterActual, tipoToken.IGUAL)
        elif self.caracterActual == '>':
            
            if self.peek() == '=':
                lastChar = self.caracterActual
                self.siguienteCaracter()
                token = Token(lastChar + self.caracterActual, tipoToken.MAYOR)
            else:
                token = Token(self.caracterActual, tipoToken.MAYORIGUAL)
        elif self.caracterActual == '<':
               
                if self.peek() == '=':
                    lastChar = self.caracterActual
                    self.siguienteCaracter()
                    token = Token(lastChar + self.caracterActual, tipoToken.MENORIGUAL)
                else:
                    token = Token(self.caracterActual, tipoToken.MENORQUE)
        elif self.caracterActual == '!':
            if self.peek() == '=':
                lastChar = self.caracterActual
                self.siguienteCaracter()
                token = Token(lastChar + self.caracterActual, tipoToken.DISTINTOA)
            else:
                self.Abortar("Esperando!=, consiguio !" + self.peek())
        elif self.caracterActual == '\"':
            
            self.siguienteCaracter()
            startPos = self.posicionActual

            while self.caracterActual != '\"':
                
                if self.caracterActual == '\r' or self.caracterActual == '\n' or self.caracterActual == '\t' or self.caracterActual == '\\' or self.caracterActual == '%':
                    self.Abortar("Carácter ilegal en cadena.")
                self.siguienteCaracter()

            tokText = self.codigo[startPos : self.posicionActual] 
            token = Token(tokText, tipoToken.STRING)
        elif self.caracterActual.isdigit():
            
            startPos = self.posicionActual
            while self.peek().isdigit():
                self.siguienteCaracter()
            if self.peek() == '.': 
                self.siguienteCaracter()

                
                if not self.peek().isdigit(): 
                    
                    self.Abortar("Caracter ilegal en numero.")
                while self.peek().isdigit():
                    self.siguienteCaracter()

            tokText = self.codigo[startPos : self.posicionActual + 1] 
            token = Token(tokText, tipoToken.NUMERO)
        elif self.caracterActual.isalpha():
            
            startPos = self.posicionActual
            while self.peek().isalnum():
                self.siguienteCaracter()

          
            tokText = self.codigo[startPos : self.posicionActual + 1] 
            keyword = Token.comprobarPalabraClave(tokText)
            if keyword == None: 
                token = Token(tokText, tipoToken.VARIABLE)
            else:   
                token = Token(tokText, keyword)
        elif self.caracterActual == '\n':
            token = Token(self.caracterActual, tipoToken.NUEVA_LINEA)
        elif self.caracterActual == '\0':
            token = Token('', tipoToken.FIN_DE_LINEA)
        else:
            
            self.Abortar("token desconocido: " + self.caracterActual)
			
        self.siguienteCaracter()
        return token



class Token:   
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   
        self.kind = tokenKind   

    @staticmethod
    def comprobarPalabraClave(tokenText):
        for kind in tipoToken:
            
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None



class tipoToken(enum.Enum):
	FIN_DE_LINEA = -1
	NUEVA_LINEA = 0
	NUMERO = 1
	VARIABLE = 2
	STRING = 3 
	# PalabrasReservadas 
	LABEL = 101
	GOTO = 102
	IMPRIMIR = 103
	ENTRADA = 104
	INT = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPETIR = 110
	ENDWHILE = 111
    
     # Operadores
	IGUALIGUAL = 201 
	SUMA = 202 
	RESTA = 203
	ASTERISCO = 204
	DIAGONAL = 205
	IGUAL = 206
	DISTINTOA = 207
	MENORQUE = 208
	MENORIGUAL = 209
	MAYOR = 210
	MAYORIGUAL = 211