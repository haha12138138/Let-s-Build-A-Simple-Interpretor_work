# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS,MINUS,MUL,DIV,EOF,LEFT_P,RIGHT_P = 'INTEGER', 'PLUS', 'MINUS','MUL','DIV','EOF','LEFT_P','RIGHT_P'
SIGN='SIGN'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char in (' ','\t','\r','\n'):
            self.__groupWhite()
            current_char = text[self.pos]# reload
            # here no white chars
        if current_char.isdigit():
            token = Token(INTEGER, self.__groupInt())
            # __groupInt has already advanced the pointer
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.advance()
            return token
        if current_char == '-':
            token= Token(MINUS,current_char)
            self.advance()
            return token
        if current_char == '*':
            token = Token(MUL, current_char)
            self.advance()
            return token
        if current_char == '/':
            token= Token(DIV,current_char)
            self.advance()
            return token
        if current_char == '(':
            token=Token(LEFT_P,current_char)
            self.advance()
            return token
        if current_char == ')':
            token=Token(RIGHT_P,current_char)
            self.advance()
            return token
        self.error()

    def __groupInt(self):
        current_char=self.text[self.pos]
        temp=0
        while current_char!=None and current_char.isdigit(): # In first iteration, current char is guaranteed to be Int
            temp=temp*10+int(current_char)
            current_char=self.advance()
        return temp

    def __groupWhite(self):
        current_char = self.text[self.pos]
        while current_char!=None and (current_char in (' ','\t','\r','\n')): # In first iteration, current char is guaranteed to be white
            current_char=self.advance()

    def advance(self):
        self.pos+=1
        if self.pos>len(self.text)-1:
            return None
        else:
            return self.text[self.pos]

    def eat(self, token_types):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type in token_types:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def sign(self):
        signtok=self.current_token
        self.eat((PLUS,MINUS))
        if signtok.type==MINUS:
            return Token(SIGN,True)
        else:
            return Token(SIGN,False)

    def number(self):
        if self.current_token.type in (PLUS,MINUS):
            sign = self.sign()
        else:
            sign=Token(SIGN,False)# positive
        termtok=self.current_token
        self.eat(INTEGER)

        if sign.value==True:
            termtok.value*=-1

        return termtok
    def factor(self):
        if self.current_token.type == LEFT_P:
            # self.eat(LEFT_P)
            lval= self.expr()
            self.eat(RIGHT_P)

        elif self.current_token.type == RIGHT_P:
            self.eat(RIGHT_P)
            print('empty term')
            self.error()
        else:
            lval=self.number()
        return lval

    def term(self):
        lval=self.factor()
        while self.current_token.type in (MUL,DIV):
            op = self.current_token
            self.eat((MUL, DIV))
            other = self.factor()
            if (op.type == MUL):
                lval.value *= other.value
            elif (op.type == DIV):
                lval.value //= other.value
        return lval
        # if peek in('+','-'):
        #     # '+'/'-' are not yet been received
        #     #this will be treated as a number
        #     return lval
        # elif peek in('*','/'):
        #     # this will be a factor subexprtion
        #     while peek in ('*','/'):
        #         op=self.current_token
        #         self.eat((MUL,DIV))
        #         other=self.number()
        #         if(op.value=='*'):
        #             lval.value*=other.value
        #         elif(op.value=='/'):
        #             lval.value//=other.value
        #         peek=self.peeknextChar()
        #     return lval
        # elif peek==None:
        #     return lval
        # self.error()
    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        self.current_token = self.get_next_token()
        # set current token to the first token taken from the input
        left = self.term()
        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            self.eat((PLUS,MINUS))
            other = self.term()
            if (op.value=='+'):
                left.value = left.value + other.value
            elif (op.value=='-'):
                left.value= left.value-other.value

        return left


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr().value
        print(result)


if __name__ == '__main__':
    main()