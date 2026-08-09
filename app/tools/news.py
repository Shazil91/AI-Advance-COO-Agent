import os
import requests
from app.tools.base import BaseTool

API_KEY=os.getenv("NEWS_API_KEY")
       
class GetNews(BaseTool):
    def name(self,name:str):
        return "news"
    
    
    def run(self,input:dict):
        country=input.get('country').lower()
        url = (
        f"https://newsapi.org/v2/top-headlines"
        f"?country={country}&apiKey={API_KEY}"
        )
        
        response=requests.get(url)
        
        if response.status_code!=200:
            return "Information not found."
        
        result=response.json()
        
        return {
            "country":country,
            "news":result,
        }