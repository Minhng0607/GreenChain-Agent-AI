import os
import json
from dotenv import load_dotenv
from crewai import Crew
from agents import scout_agent, financial_agent, AgentFactory
from tasks import create_scout_task, create_finance_task


def run_scout_workflow(trash_list=None):
    """Run CrewAI workflow with scout and financial agents."""
    load_dotenv()

    if scout_agent is None or financial_agent is None:
        raise RuntimeError("Agents not initialized. Check GOOGLE_API_KEY and agent module.")

    # Prepare sample trash data
    if trash_list is None:
        trash_list = [
            "plastic water bottle",
            "aluminum soda can",
            "paperboard cereal box",
            "glass jam jar",
            "styrofoam food container"
        ]

    # Create tasks in correct order: Scout first, then Finance
    scout_task = create_scout_task(trash_list)
    finance_task = create_finance_task()
    
    # Create crew with both agents and tasks in the correct order
    crew = Crew(
        agents=[scout_agent, financial_agent],
        tasks=[scout_task, finance_task],
        verbose=True
    )

    # Execute tasks
    print("Running multi-agent workflow with Scout and Finance agents...")
    result = crew.kickoff()

    # Parse the final result
    final_result = None
    if isinstance(result, str):
        try:
            final_result = json.loads(result)
            print("Task result (JSON):")
            print(json.dumps(final_result, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Task returned non-JSON text. Raw output:")
            print(result)
            final_result = result
    else:
        print("Task result (object):")
        print(result)
        final_result = result

    # Combine scout and finance results for the UI
    combined_result = {}
    
    # Try to read scout output from file
    try:
        if os.path.exists("scout_analysis_output.json"):
            with open("scout_analysis_output.json", "r") as f:
                scout_data = json.load(f)
                combined_result["scout_task"] = scout_data
                print(f"[main.py] Loaded scout data from file: {len(scout_data) if isinstance(scout_data, list) else 'dict'} items")
    except Exception as e:
        print(f"[main.py] Could not load scout data: {e}")
    
    # Add finance result
    if isinstance(final_result, dict):
        combined_result["finance_task"] = final_result
    else:
        combined_result["finance_task"] = None
    
    print(f"[main.py] Combined result keys: {list(combined_result.keys())}")
    return combined_result if combined_result else final_result


if __name__ == "__main__":
    try:
        run_scout_workflow()
    except Exception as e:
        print(f"ERROR: {e}")
