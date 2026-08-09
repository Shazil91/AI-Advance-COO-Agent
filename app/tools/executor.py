import json

from app.tools.registry import ToolRegistry

registry = ToolRegistry()


def extract_tool_call(text: str):
    """
    Expected Gemini output:

    TOOL: gmail
    INPUT: {"to":"abc@gmail.com","subject":"Hello","body":"Hi"}
    """

    try:
        # Planner didn't request any tool
        if "TOOL:" not in text or "INPUT:" not in text:
            return None

        lines = text.splitlines()

        tool_line = next(
            line for line in lines if line.startswith("TOOL:")
        )

        input_line = next(
            line for line in lines if line.startswith("INPUT:")
        )

        tool_name = tool_line.replace("TOOL:", "").strip()

        input_data = json.loads(
            input_line.replace("INPUT:", "").strip()
        )

        return tool_name, input_data

    except Exception as e:
        print("Error while parsing tool call:", e)
        print("Planner output was:")
        print(text)
        return None


def run_tool_or_llm(prompt: str):

    if not prompt or prompt.strip() == "":
        return "ERROR: Empty planner response."

    tool_call = extract_tool_call(prompt)

    if tool_call:

        tool_name, input_data = tool_call

        tool = registry.get(tool_name)

        if tool:
            return tool.run(input_data)

        return f"ERROR: Tool '{tool_name}' is not registered."

    # Planner returned normal text
    return prompt