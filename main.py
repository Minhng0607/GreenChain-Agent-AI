import os
import json
from dotenv import load_dotenv
from crewai import Crew
from agents import scout_agent, AgentFactory
from tasks import create_scout_task


def run_scout_workflow(trash_list=None):
    """Run CrewAI workflow with scout agent and material analysis task."""
    load_dotenv()

    if scout_agent is None:
        raise RuntimeError("scout_agent is not initialized. Check GOOGLE_API_KEY and agent module.")

    # Prepare sample trash data
    if trash_list is None:
        trash_list = [
            "plastic water bottle",
            "aluminum soda can",
            "paperboard cereal box",
            "glass jam jar",
            "styrofoam food container"
        ]

    # Create task and crew
    task = create_scout_task(trash_list)
    crew = Crew(agents=[scout_agent], tasks=[task], verbose=True)

    # Execute task
    print("Running scout task with Gemin i 3 Flash optimized CrewAI flow...")
    result = crew.kickoff()

    # `result` may be object/str depending on CrewAI implementation; attempt JSON parse
    if isinstance(result, str):
        try:
            parsed = json.loads(result)
            print("Task result (JSON):")
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Task returned non-JSON text. Raw output:")
            print(result)
    else:
        print("Task result (object):")
        print(result)

    return result


if __name__ == "__main__":
    try:
        run_scout_workflow()
    except Exception as e:
        print(f"ERROR: {e}")
