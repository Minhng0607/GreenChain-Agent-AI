"""
GreenChain Task Definitions
Task definitions for waste material analysis and ESG compliance
Built for GDGoC Hackathon Vietnam 2026
"""

from crewai import Task
from agents import scout_agent


# ============================================================================
# WASTE MATERIAL ANALYSIS TASK
# ============================================================================

def create_scout_task(trash_list: str | list = None) -> Task:
    """
    Create a scout task for waste material analysis.
    
    This task analyzes a list of waste materials and generates:
    - Material type identification
    - Recyclability scoring (0-100)
    - ESG impact assessment
    
    Args:
        trash_list: List of waste items or a string representation of items.
                   If None, uses a default sample list.
    
    Returns:
        Configured Task instance linked to scout_agent
    """
    # Format trash list for task description
    if isinstance(trash_list, list):
        trash_list_str = ", ".join(trash_list)
    elif trash_list is None:
        trash_list_str = "plastic water bottle, aluminum can, paper cardboard box, glass jar"
    else:
        trash_list_str = str(trash_list)
    
    return Task(
        description=(
            f"Analyze the following waste materials: {trash_list_str}\n\n"
            "For EACH item, provide:\n"
            "1. Material Type: Identify the primary material composition\n"
            "2. Recyclability Score: Calculate a score from 0-100 where:\n"
            "   - 0-25: Not recyclable or extremely difficult\n"
            "   - 26-50: Limited recyclability potential\n"
            "   - 51-75: Moderately recyclable with standard processes\n"
            "   - 76-100: Highly recyclable, widely accepted\n"
            "3. ESG Impact Statement: One concise sentence about environmental/social/governance impact\n\n"
            "CRITICAL: Return output as valid JSON ONLY. No other text.\n"
            "Ensure JSON is properly formatted and can be parsed by Python's json module."
        ),
        expected_output=(
            "A valid JSON array containing objects with this exact structure:\n"
            "[\n"
            "  {\n"
            "    \"item_name\": \"string\",\n"
            "    \"material\": \"string\",\n"
            "    \"recyclability_score\": integer (0-100),\n"
            "    \"esg_impact\": \"string (single sentence)\"\n"
            "  },\n"
            "  ...\n"
            "]\n\n"
            "IMPORTANT: Return ONLY valid JSON. No markdown, no explanations, no code blocks."
        ),
        agent=scout_agent,
        output_file="scout_analysis_output.json"
    )


# ============================================================================
# TASK FACTORY
# ============================================================================

class TaskFactory:
    """Factory for creating and managing tasks."""
    
    @staticmethod
    def get_scout_task(trash_list: str | list = None) -> Task:
        """
        Get a new scout task instance.
        
        Args:
            trash_list: List of waste items to analyze
        
        Returns:
            Configured scout Task
        """
        return create_scout_task(trash_list)
    
    @staticmethod
    def list_tasks() -> list[str]:
        """Get list of available task types."""
        return ["scout"]


# ============================================================================
# PREDEFINED TASKS
# ============================================================================

# Default scout task with sample materials
scout_task = create_scout_task()


__all__ = [
    "create_scout_task",
    "scout_task",
    "TaskFactory",
]
