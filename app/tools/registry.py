from app.tools.gmail import GmailTool
from app.tools.calender import CalendarTool
from app.tools.weather import GetWeather
from app.tools.news import GetNews
class ToolRegistry:

    def __init__(self):
        self.tools = {
            "gmail": GmailTool(),
            "calendar": CalendarTool(),
            "weather": GetWeather(),
            "news": GetNews(),
        }

    def get(self, name: str):
        return self.tools.get(name)