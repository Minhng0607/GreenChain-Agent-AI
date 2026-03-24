"""
GreenChain Agent System
Agentic AI for automated ESG compliance and waste recycling management
Built for GDGoC Hackathon Vietnam 2026

This module provides CrewAI agents configured with Google Gemini 3 Flash
for sustainable waste management and ESG compliance tasks.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables immediately during module import to avoid missing keys
load_dotenv()


# ============================================================================
# ENVIRONMENT & INITIALIZATION
# ============================================================================

def load_environment() -> None:
    """Load environment variables from .env file."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")


def initialize_llm(
    model_name: str = "gemini-3-flash-preview",
    temperature: float = 0.7,
    max_tokens: int = 2048
) -> ChatGoogleGenerativeAI:
    """
    Initialize ChatGoogleGenerativeAI with CrewAI compatibility.

    Tries model "gemini-3-flash-preview" first, then "gemini-1.5-flash" fallback.

    Args:
        model_name: The preferred Google Generative AI model to use.
        temperature: Controls randomness (0.0-1.0).
        max_tokens: Maximum tokens in response.

    Returns:
        Initialized ChatGoogleGenerativeAI instance.

    Raises:
        ValueError: If GOOGLE_API_KEY is not set.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")

    preferred_models = [model_name, "gemini-1.5-flash"]
    last_exception = None

    for candidate in preferred_models:
        try:
            llm = ChatGoogleGenerativeAI(
                model=candidate,
                temperature=temperature,
                max_tokens=max_tokens,
                google_api_key=api_key
            )
            # ensure model is valid by minimal request to init, if supported by provider
            return llm
        except Exception as exc:
            last_exception = exc

    raise RuntimeError(
        "Failed to initialize ChatGoogleGenerativeAI with gemini-3-flash-preview or gemini-1.5-flash. "
        + "Last error: " + str(last_exception)
    )


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

def create_scout_agent(llm: Optional[ChatGoogleGenerativeAI] = None) -> Agent:
    """
    Create an ESG & Material Specialist Scout Agent.

    Role: Scout and assess materials for environmental, social, and governance (ESG) compliance
    
    Responsibilities:
    - Analyze material composition and properties
    - Evaluate environmental impact across lifecycle (production, use, disposal)
    - Assess recyclability and circular economy potential
    - Identify ESG compliance gaps and opportunities
    - Provide initial recommendations for waste categorization
    
    Args:
        llm: The language model instance
    
    Returns:
        Configured Agent instance for ESG and material analysis
    """
    # CrewAI may require string model reference for llm to avoid pydantic mismatches:
    model_ref = "google/gemini-3-flash-preview"
    if llm is None:
        # Fallback if direct object injection is needed for other code paths
        try:
            _ = initialize_llm(model_name="gemini-3-flash-preview")
            model_ref = "google/gemini-3-flash-preview"
        except Exception:
            model_ref = "google/gemini-1.5-flash"

    return Agent(
        role="ESG & Material Specialist",
        goal="Identify, analyze, and assess materials for ESG compliance, sustainability potential, and recyclability within the circular economy framework",
        backstory=(
            "You are a certified ESG specialist with expertise in material science, "
            "sustainability assessment, and circular economy principles. With credentials "
            "equivalent to HUST's Environmental Engineering standards, you conduct rigorous "
            "evaluations of material composition, environmental footprint, and social responsibility. "
            "Your assessments follow ISO 14001, GRI, and SASB frameworks. You excel at identifying "
            "materials that align with ESG standards, quantifying environmental impact, and "
            "recommending sustainable alternatives and recycling pathways."
        ),
        llm=model_ref,
        verbose=False,
        allow_delegation=False,
        max_iter=10,
        memory=True
    )


def create_analyzer_agent(llm: Optional[ChatGoogleGenerativeAI] = None) -> Agent:
    """
    Create a Waste & Recycling Analyzer Agent.
    
    Role: Analyze waste streams and optimize recycling strategies
    
    Responsibilities:
    - Evaluate waste stream composition and characteristics
    - Determine optimal recycling and processing methods
    - Assess technical and economic feasibility
    - Identify waste reduction opportunities
    - Recommend resource recovery strategies
    
    Args:
        llm: The language model instance
    
    Returns:
        Configured Agent instance for waste analysis
    """
    model_ref = "google/gemini-3-flash-preview"
    if llm is None:
        try:
            _ = initialize_llm(model_name="gemini-3-flash-preview")
            model_ref = "google/gemini-3-flash-preview"
        except Exception:
            model_ref = "google/gemini-1.5-flash"

    return Agent(
        role="Waste & Recycling Analyst",
        goal="Analyze waste streams and design optimal recycling strategies that maximize resource recovery and minimize environmental impact",
        backstory=(
            "You are a waste management specialist with deep expertise in recycling processes, "
            "waste stream analysis, and circular economy optimization. Your analytical background "
            "combines engineering principles with sustainability science. You evaluate the technical "
            "feasibility and economic viability of recycling different materials, recommend "
            "processing methods, and identify opportunities for waste reduction and resource recovery."
        ),
        llm=model_ref,
        verbose=False,
        allow_delegation=False,
        max_iter=10,
        memory=True
    )


def create_compliance_agent(llm: Optional[ChatGoogleGenerativeAI] = None) -> Agent:
    """
    Create an ESG Compliance Auditor Agent.
    
    Role: Verify ESG compliance and generate compliance documentation
    
    Responsibilities:
    - Audit processes and materials against ESG standards
    - Verify compliance with international regulations
    - Identify compliance gaps and risks
    - Generate compliance reports and documentation
    - Recommend remediation strategies
    
    Args:
        llm: The language model instance
    
    Returns:
        Configured Agent instance for compliance auditing
    """
    model_ref = "google/gemini-3-flash-preview"
    if llm is None:
        try:
            _ = initialize_llm(model_name="gemini-3-flash-preview")
            model_ref = "google/gemini-3-flash-preview"
        except Exception:
            model_ref = "google/gemini-1.5-flash"

    return Agent(
        role="ESG Compliance Auditor",
        goal="Ensure all processes, materials, and practices meet international ESG standards and regulatory requirements",
        backstory=(
            "You are a certified ESG compliance auditor with extensive knowledge of international "
            "standards including ISO 14001, GRI Standards, SASB Frameworks, and regional regulations. "
            "Your expertise spans environmental law, social governance, and sustainable business practices. "
            "You conduct thorough compliance assessments, identify regulatory gaps, and provide "
            "comprehensive recommendations for achieving and maintaining ESG certification."
        ),
        llm=model_ref,
        verbose=False,
        allow_delegation=False,
        max_iter=10,
        memory=True
    )


# ============================================================================
# AGENT FACTORY
# ============================================================================

class AgentFactory:
    """Factory for creating and managing CrewAI agents."""
    
    def __init__(self, llm: Optional[ChatGoogleGenerativeAI] = None):
        """
        Initialize the AgentFactory with an LLM instance.
        
        Args:
            llm: Optional pre-initialized LLM instance.
                 If None, initializes a new instance with default settings.
        """
        load_environment()
        self.llm = llm or initialize_llm()
        self._agents = {}
    
    def get_agent(self, agent_type: str) -> Agent:
        """
        Get or create an agent of the specified type.
        
        Args:
            agent_type: Type of agent ('scout', 'analyzer', 'compliance')
        
        Returns:
            Agent instance
        
        Raises:
            ValueError: If agent_type is not recognized
        """
        if agent_type in self._agents:
            return self._agents[agent_type]
        
        if agent_type == "scout":
            agent = create_scout_agent(self.llm)
        elif agent_type == "analyzer":
            agent = create_analyzer_agent(self.llm)
        elif agent_type == "compliance":
            agent = create_compliance_agent(self.llm)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        self._agents[agent_type] = agent
        return agent
    
    def list_agents(self) -> list[str]:
        """Get list of available agent types."""
        return ["scout", "analyzer", "compliance"]


# ============================================================================
# MODULE EXPORTS
# ============================================================================

# Initialize default factory for convenience imports
try:
    print("[agents.py] load_environment() start")
    load_environment()
    print("[agents.py] load_environment() success")

    _default_llm = initialize_llm()
    print(f"[agents.py] LLM initialized with model: {_default_llm.model}")

    _default_factory = AgentFactory(_default_llm)
    print("[agents.py] AgentFactory created")

    # Export scout agent for direct import
    scout_agent = _default_factory.get_agent("scout")
    analyzer_agent = _default_factory.get_agent("analyzer")
    compliance_agent = _default_factory.get_agent("compliance")
    print("Agent initialized successfully")

except Exception as e:
    print(f"[agents.py] Initialization failed: {e}")
    # Allow module import even if environment is not configured
    scout_agent = None
    analyzer_agent = None
    compliance_agent = None


__all__ = [
    "AgentFactory",
    "initialize_llm",
    "load_environment",
    "create_scout_agent",
    "create_analyzer_agent",
    "create_compliance_agent",
    "scout_agent",
    "analyzer_agent",
    "compliance_agent",
]

 