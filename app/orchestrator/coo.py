import re
from app.agents.planner_agent import PlannerAgent
from app.memory.memory import MemoryEngine
from app.tools.executor import run_tool_or_llm


class COOAgent:

    def __init__(self):
        self.planner = PlannerAgent()
        self.memory = MemoryEngine()

    # -----------------------------
    # MAIN COO ENGINE
    # -----------------------------
    def process(self, query: str):

        # -----------------------------
        # 🧠 STEP 0: AUTO SAVE CONTACT
        # -----------------------------
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', query)

        if email_match:
            email = email_match.group()

            words = query.split()
            if "to" in words:
                idx = words.index("to")
                if idx + 1 < len(words):
                    name = words[idx + 1]

                    # Avoid saving email as name
                    if "@" not in name:
                        try:
                            self.memory.add_contact(name, email)
                        except:
                            pass

        # -----------------------------
        # 🧠 STEP 1: AUTO REPLACE NAME → EMAIL
        # -----------------------------
        words = query.split()

        for word in words:
            contact = self.memory.get_contact(word)
            if contact:
                query = query.replace(word, contact.email)

        # -----------------------------
        # 🧠 STEP 2: LOAD MEMORY CONTEXT
        # -----------------------------
        memories = self.memory.get_recent_memories()
        memory_text = "\n".join([m.content for m in memories])

        context = f"""
        You are an AI COO with tool access.

        MEMORY:
        {memory_text}

        USER REQUEST:
        {query}

        IMPORTANT:
        - If action needed → return TOOL format
        - NEVER return empty
        """

        # -----------------------------
        # 🧠 STEP 3: GET PLAN
        # -----------------------------
        plan = self.planner.run(context)

        # ❗ SAFETY CHECK
        if not plan or plan.strip() == "":
            return {
                "error": "Planner returned empty response",
                "query": query
            }

        # -----------------------------
        # ⚙️ STEP 4: EXECUTE TOOL
        # -----------------------------
        try:
            execution = run_tool_or_llm(plan)
        except Exception as e:
            return {
                "error": str(e),
                "plan": plan
            }

        # -----------------------------
        # 💾 STEP 5: SAVE MEMORY
        # -----------------------------
        try:
            self.memory.save_memory("execution", str(execution))
        except:
            pass

        # -----------------------------
        # ✅ FINAL RESPONSE
        # -----------------------------
        return {
            "plan": plan,
            "execution": execution
        }