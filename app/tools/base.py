from abc import ABC,abstractmethod

class BaseTool(ABC):
    @abstractmethod
    def name(self)->str:
        pass 
    
    @abstractmethod
    def run(self,input_data:dict):
        pass
    
    