from collections import defaultdict

class Equation:
    def __init__(self, dict_eq:dict|defaultdict=defaultdict(float)):
        self.dict: defaultdict = defaultdict(float, dict_eq)

    @property
    def variables(self):
        return self.dict.keys()
    
    def get_line(self, variables):
        return [self[v] for v in variables]
    
    def __eq__(self, other):
        if type(other) == type(self):
            return self.dict == other.dict
        return super().__eq__(other) 
    
    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value
        if self.dict[key] == 0:
            self.dict.pop(key)

    def __mul__(self, other):
        for key in self.dict:
            self[key] *= other
        return self

    def __add__(self, other):
        for key in other:
            self[key] += other[key]
        return self

    def __contains__(self, key):
        return key in self.dict
    
    def __iter__(self):
        return iter(self.dict)
    
    def __str__(self):
        return ' + '.join([ f'{self.dict[k]} {(f"({k.name})" if " " in k.name else k.name) if type(k).__name__ in ['Node', 'Loop'] else (f"i{'{'}{k[0].name}{'}'}")}' for k in self.dict if k is not None ]) + f' = {-self.dict[None] if None in self else 0}'
    
    def equal(self, other):
        if type(other) == type(self):
            return self.dict == other.dict
        return False

