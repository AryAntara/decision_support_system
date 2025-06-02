from abc import ABC, abstractmethod
import pandas as pd
import copy

class Validation: 
    def is_int(self, num: int) -> bool: 
        return isinstance(num, int)
    
    def is_str(self,text: str) -> bool: 
        return isinstance(text, str)
    
    def is_bool(self, statement: bool) -> bool: 
        return isinstance(statement, int)
    
    def is_float(self, point: float) -> bool: 
        return isinstance(point, float)
    
    def is_all_number(self, data: list) -> bool:
        return isinstance(data, list) and all(self.is_float(num) or self.is_int(num) for num in data)
    
    def is_all_string(self, data: list) -> bool:
        return isinstance(data, list) and all(self.is_str(text) for text in data)
    
    def is_len_match(self, *cols: list) -> bool: 
        length = len(cols[0]) 
        return all(length == len(data) for data in cols[1:]) 
    
    def is_in_options(self, data: list, options: list[str]) -> bool:
        return isinstance(data, list) and all(val in options for val in data)
        

class Model(Validation):
    
    # the data is headings label of data
    @property
    @abstractmethod
    def data(self) -> dict[any]: pass
    
    # needs to validate the data to check their usability
    @abstractmethod
    def validate(self, data: dict[any]) -> bool : pass

    def length(self) -> int: 
        return len(self.get_names())
    
    def get_data(self) -> dict: 
        return copy.deepcopy(self.data)

    

   