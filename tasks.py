"""
GreenChain Task Definitions
Task definitions for waste material analysis and ESG compliance
Built for GDGoC Hackathon Vietnam 2026
"""

from crewai import Task
from agents import scout_agent, financial_agent


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
# FINANCIAL ANALYSIS TASK
# ============================================================================

def create_finance_task(scout_output: str | list = None, context: str = "scout_task") -> Task:
    """
    Create a finance task for calculating monetary rewards from recycled materials.
    
    This task analyzes the output from scout_task and calculates:
    - Total monetary reward based on material types and quantities
    - Financial advice on recycling initiatives
    
    Financial rates:
    - Plastic: $0.05/unit
    - Aluminum: $0.15/unit
    - Paper: $0.02/unit
    
    Args:
        scout_output: Output from scout_task (JSON string or list) containing material analysis.
                     Can be a string representation or actual data.
        context: Context information about how to process the scout_task output.
    
    Returns:
        Configured Task instance linked to financial_agent
    """
    if isinstance(scout_output, list):
        scout_output_str = str(scout_output)
    elif scout_output is None:
        scout_output_str = "[scout_task output will be provided here]"
    else:
        scout_output_str = str(scout_output)
    
    return Task(
        description=(
            f"Based on the following scout analysis output:\n{scout_output_str}\n\n"
            "Calculate the total monetary reward for recycled materials using these rates:\n"
            "- Plastic: $0.05 per unit\n"
            "- Aluminum: $0.15 per unit\n"
            "- Paper: $0.02 per unit\n\n"
            "For EACH item from the scout analysis:\n"
            "1. Identify the material type (extract from 'material' field)\n"
            "2. Assign a unit count based on recyclability_score if item name suggests quantity, or default to 1 unit\n"
            "3. Apply the corresponding rate to calculate reward for that item\n"
            "4. Sum all rewards to get total monetary reward\n\n"
            "Provide financial advice (1-2 sentences) on the monetary reward and recycling value.\n\n"
            "CRITICAL: Return output as valid JSON ONLY. No other text.\n"
            "Ensure JSON is properly formatted and can be parsed by Python's json module."
        ),
        expected_output=(
            "A valid JSON object with this exact structure:\n"
            "{\n"
            "  \"total_reward\": number (in USD),\n"
            "  \"Financial Advice\": \"string (1-2 sentences about financial reward and recycling value)\"\n"
            "}\n\n"
            "IMPORTANT: Return ONLY valid JSON. No markdown, no explanations, no code blocks."
        ),
        agent=financial_agent,
        output_file="finance_analysis_output.json"
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
    def get_finance_task(scout_output: str | list = None) -> Task:
        """
        Get a new finance task instance.
        
        Args:
            scout_output: Output from scout_task to analyze
        
        Returns:
            Configured finance Task
        """
        return create_finance_task(scout_output)
    
    @staticmethod
    def list_tasks() -> list[str]:
        """Get list of available task types."""
        return ["scout", "finance"]


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
