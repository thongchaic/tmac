
import random

class Tokens:
    def __init__(self):
        self.tokens = {}
    
    def add(self,_MAC, r=None):
        if r is None:
            r = str(random.random())
        self.tokens[_MAC] = r 
        return r 
    
    def delete(self, _MAC):
        if _MAC in self.tokens:
            self.tokens.pop(_MAC)

    def get(self,_MAC):
        if _MAC in self.tokens:
            return self.tokens[_MAC]
        return None
        
    def all(self):
        if len(self.tokens) <=0:
            return None 
        return self.toekns