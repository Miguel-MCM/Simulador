from collections import defaultdict

class Equation:
    def __init__(self, dict_eq:dict|defaultdict=None):
        self.dict: defaultdict = dict_eq if dict_eq is not None else defaultdict(float)
    
    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value
        if self.dict[key] == 0:
            self.dict.pop(key)

    def __mul__(self, other):
        for key in self.dict:
            self[key] *= other
        return self.dict

    def __contains__(self, key):
        return key in self.dict
    
    def __iter__(self):
        return iter(self.dict)
    
    def __str__(self):
        return ' + '.join([ f'{self.dict[k]}({k.name})' for k in self.dict if k is not None ]) + f' = {self.dict[None] if None in self else 0}'
    


