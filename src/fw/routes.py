
import random

class Routes:
    def __init__(self):
        self.routes = {}
    
    def add(self,_MAC, _TYPE=None):
        print(" ::Routes add=>",_MAC, _TYPE)
        self.routes[_MAC] = _TYPE
        return _TYPE
    
    def delete(self, _MAC):
        if _MAC in self.routes:
            self.routes.pop(_MAC)

    def get(self,_MAC, _TYPE="gw"):
        if _MAC in self.routes:
            return self.routes[_MAC]
        return None
    
    def gw(self):
        for r in self.routes:
            if self.routes[r] == "gw":
                return r
        return None 
        
    def all(self):
        if len(self.routes) <=0:
            return None 
        return self.routes