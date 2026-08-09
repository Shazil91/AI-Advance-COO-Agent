from app.core.gemini import ask_gemini

class PlannerAgent:

    def run(self, context: str):

       prompt = f"""
       You are an AI COO.

       YOU MUST ALWAYS RETURN A RESPONSE.

       If tool is needed:

       TOOL: gmail
       INPUT: {{"to":"email","subject":"hello","body":"hello"}}

       If calendar:

       TOOL: calendar
       INPUT: {{"title":"meeting","date":"today","time":"2pm"}}
       
       if weather:
       
       TOOL: weather
       INPUT: {{"city":"Karachi"}}
       
       if news:
       
       TOOL: news
       INPUT: {{"country":"us"}}
       
       NEVER return empty.
       NEVER return null.
       NEVER return explanation.

       Context:
       {context}
       """

       response = ask_gemini(prompt)

    # ❗ SAFETY CLEANUP
       if not response:
          return "TOOL: gmail\nINPUT: {\"to\":\"test@example.com\",\"subject\":\"hello\",\"body\":\"hello\"}"

       return response
   
   