# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 14:58:44 2024

@author: lcuev
"""
import keywords as kw
from token_ import Token, RESERVED_KEYWORDS


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception(f'Invalid character {self.current_char}')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum()):
            result += self.current_char
            self.advance()
        
        if result in RESERVED_KEYWORDS.keys():
            return RESERVED_KEYWORDS[result]
        elif self.current_char == '[':
            token = Token(kw.REF,Token(kw.ID,result))
            self.advance()
        else:
            token = Token(kw.ID,result)
            
        return token
    
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return Token(kw.INT, self.integer())

            if self.current_char == '=':
                self.advance()
                return Token(kw.ASSIGN, '=')

            if self.current_char == ';':
                self.advance()
                return Token(kw.SEMI, ';')
            
            if self.current_char == '^':
                self.advance()
                return Token(kw.UPCAR, '^')
            
            if self.current_char == ',':
                self.advance()
                return Token(kw.COMMA, ',')

            if self.current_char == '+':
                self.advance()
                return Token(kw.ADD, '+')

            if self.current_char == '-':
                self.advance()
                return Token(kw.SUB, '-')

            if self.current_char == '*':
                self.advance()
                return Token(kw.MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(kw.DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(kw.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(kw.RPAREN, ')')
            
            if self.current_char == '{':
                self.advance()
                return Token(kw.LBRACK, '{')
            
            if self.current_char == '}':
                self.advance()
                return Token(kw.RBRACK, '}')
            
            if self.current_char == '[':
                self.advance()
                return Token(kw.LBRACE, '[')
            
            if self.current_char == ']':
                self.advance()
                return Token(kw.RBRACE, ']')
            
            if self.current_char == '&':
                self.advance()
                return Token(kw.DIF,'&')
            
            if self.current_char == '$' and self.peek() == '_':
                self.advance()
                self.advance()
                return Token(kw.PART,'$')

            self.error()

        return Token(kw.EOF, None)
    
    def reset(self):
        self.pos = 0
        self.current_char = self.text[self.pos]

