class Names(object):
    def __init__(self):
        self.names={}  #| MAC | Type | ID | Name |
                
    def add(self, _MAC, _id, _name, _type):
        if _MAC in self.names:
            for i,n,t in self.names[_MAC]:
                if _id == i and n == _name and _type == t:
                    return 
            self.names[_MAC].append( (_id, _name, _type) )
        else:
            self.names[_MAC] = [ (_id, _name, _type) ]
        #self.show()
        
    def show(self):
        print(self.names)

    def flush(self, _MAC):
        if _MAC in self.names:
            self.names.pop(_MAC)

    def get(self,_MAC, _id):
        if _MAC in self.names:
            for id, name, _type in self.names[_MAC]:
                if id == _id:
                    return name, _type
        return None, None 

    def gw(self):
        for _MAC in self.names:
            for id, name, _type in self.names[_MAC]:
                if _type == 1:
                    return _MAC
        return None 