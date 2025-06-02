from models import model 
from models import criteria as ctr
import pandas as pd


class AlternativeModel(model.Model): 
    data: dict[any] = {}
    criteria: ctr.CriteriaModel
    
    def __init__(self, data: list[int], criteria: ctr.CriteriaModel): 
        
        self.data = {
            "Crit": criteria.get_names()
        }
                  
        for i, name in enumerate(data.keys()):             
            code = f"A{i + 1}"
            self.data[code] = data[name]
    
        self.criteria = criteria                
        (message, success) = self.validate()
        if(not success): raise Exception(message)
    
    def get_codes(self) -> list: 
        codes = [] 
        for i, key in enumerate(self.data.keys()):
            if i == 0: continue
            codes.append(key)
        return codes

    def validate(self):
        data = self.data 
        ctr = self.criteria
        ctr_len = ctr.length()
        for name in data.keys():
        
            if(name == "Crit"): continue        
            entry = data[name];            
            if(ctr_len != len(entry)):
                return ("Data length not enough", False)
            
            if(not self.is_all_number(entry)): 
                return ("Not all of weight is number", False)
        
        return ("Validation success", True)
            
    