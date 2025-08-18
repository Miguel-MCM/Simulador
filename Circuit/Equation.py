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

    def to_latex(self, loop_analysis=False):
        """
        Converte a equação para formato LaTeX.
        
        Args:
            loop_analysis (bool): Se True, formata para análise de malhas
                                 Se False, formata para análise nodal
        
        Returns:
            str: Equação em formato LaTeX
        """
        terms = []
        
        for k in self.dict:
            if k is None:
                continue
                
            coeff = self.dict[k]
            
            # Formata o coeficiente
            if coeff == 1:
                coeff_str = ""
            elif coeff == -1:
                coeff_str = "-"
            else:
                coeff_str = f"{coeff}"
            
            # Formata a variável
            if type(k).__name__ in ['Node', 'Loop']:
                # Para nós e malhas
                if " " in k.name:
                    var_str = f"({k.name})"
                else:
                    var_str = k.name
            else:
                # Para correntes (assumindo que k é uma tupla com o primeiro elemento sendo o nome)
                if hasattr(k, '__getitem__') and len(k) > 0:
                    var_str = f"i_{{{k[0].name}}}"
                else:
                    var_str = str(k)
            
            # Monta o termo
            if coeff_str == "":
                term = var_str
            elif coeff_str == "-":
                term = f"-{var_str}"
            else:
                term = f"{coeff_str}{var_str}"
            
            terms.append(term)
        
        # Monta o lado esquerdo da equação
        left_side = " + ".join(terms) if terms else "0"
        left_side = left_side.replace(" + -", " - ")
        
        # Monta o lado direito da equação
        if None in self.dict:
            right_side = f"{-self.dict[None]}"
        else:
            right_side = "0"
        
        return f"{left_side} = {right_side}"
