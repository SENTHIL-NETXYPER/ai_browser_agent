from llm_service import decide_action
from tool_router import run_tool

def run_agent():

    user_prompt = input("Enter instruction: ")

    action = decide_action(user_prompt)

    print("AI Decision:", action)

    run_tool(action)


run_agent()