from sqlmodel import Session
from app.memory.db import engine
from app.memory.models import Memory,Goal,Contact
from sqlmodel import select
class MemoryEngine:
    def __init__(self):
        self.db = Session(engine)

    def save_memory(self,type_:str,content:str):
        memory=Memory(type=type_,content=content)
        self.db.add(memory)
        self.db.commit()
    
    def get_recent_memories(self,limit:int=5):
        statement=select(Memory).order_by(Memory.id.desc()).limit(limit)
        return  self.db.exec(statement).all()
   
    def add_goal(self,goal:str):
       new_goal=Goal(goal=goal)
       self.db.add(new_goal)
       self.db.commit()
       
    def get_goal(self):
        statemment=select(Goal)
        return self.db.exec(statemment).all()
    
    def add_contact(self,name:str,email:str):
        new_contact=Contact(name=name,email=email)
        self.db.add(new_contact)
        self.db.commit()
        
        
    def get_contact(self,name:str):
        statement=select(Contact).where(Contact.name==name.lower())
        return self.db.exec(statement).first()