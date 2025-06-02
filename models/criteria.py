from models import model 
import pandas as pd


class CriteriaModel(model.Model): 
    
    data: dict[any] = {}
    
    def __init__(self, data: dict[any]): 
        self.data = data
         
        (message, success) = self.validate()
        if(not success):
            raise Exception(message)
                
    def get_weights(self) -> list[str]: 
        return self.data.get("weight")
    
    def get_types(self) -> list[str]: 
        return self.data.get("type")
    
    def get_labels(self) -> list[str]: 
        return self.data.get("label")
                
    def get_names(self) -> list[str]: 
        return self.data.get("name")
    
    def find_one_weight_by_name(self, name: str) -> int|float:   
        idx = 0         
        
        # getting index of this name
        for i, v in enumerate(self.get_names()):               
            if v is name: idx=i 
                    
        # return the weight follow the index                
        return self.get_weights()[idx]
        
    def validate(self) -> tuple[str, bool]:  
        data = self.data 
        
        if(not all(key in ["type", "name", "weight", "label"] for key in data.keys())): 
            return ("Please provide a dict with 'label', 'type', 'name', and 'weight'", False)
        
        if(not self.is_in_options(data.get("type"), ["COST", "BENEFIT"])): 
             return ("Some of types is invalid", False);   
         
        if(not self.is_len_match(data.get("label"), data.get("name"), data.get("weight"), data.get("type"))): 
            return ("Data length doesn't match each others", False)
     
        if(not self.is_all_string(data.get("label"))): 
            return ("Column label must be all of string", False) 
            
        if(not self.is_all_string(data.get("name"))): 
            return ("Column name must be all of string", False) 
        
        if(not self.is_all_number(data.get("weight"))): 
            return ("Column weight must be all of number", False)
        
        return ("Validation success", True)
        
    
        