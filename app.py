"""
Green Chain ESG Assistant Frontend
Web interface powered by Streamlit for waste recycling and ESG analysis
Built for GDGoC Hackathon Vietnam 2026
"""

import streamlit as st
import json
import pandas as pd
from main import run_scout_workflow

# Page configuration
st.set_page_config(
    page_title="Green Chain ESG Assistant",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTitle {
        color: #2E7D32;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🌱 Green Chain ESG Assistant")
st.markdown("---")

# Sidebar
st.sidebar.header("About")
st.sidebar.markdown("""
### Green Chain System
A multi-agent AI system for:
- 📊 ESG compliance analysis
- ♻️ Waste material assessment
- 💰 Financial reward calculation
- 🌍 Circular economy solutions

**Technology Stack:**
- CrewAI for multi-agent orchestration
- Google Gemini 3 Flash LLM
- Streamlit for web interface
""")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Waste Analysis Input")
    st.markdown("Enter a list of waste items or materials you want to analyze for recycling potential and financial rewards.")
    
    # Text input for trash list
    trash_input = st.text_area(
        "Enter trash items (comma-separated or line-by-line):",
        value="plastic water bottle, aluminum soda can, paperboard cereal box, glass jam jar",
        height=100,
        placeholder="E.g., plastic bottle, aluminum can, paper box..."
    )

with col2:
    st.subheader("⚙️ Settings")
    st.markdown("**Input Format:**")
    st.info("Paste items separated by commas or each on a new line")

# Parse input
def parse_trash_list(input_str):
    """Parse trash list from text input."""
    if not input_str.strip():
        return []
    
    # Try comma-separated first
    if "," in input_str:
        items = [item.strip() for item in input_str.split(",") if item.strip()]
    else:
        # Otherwise split by newline
        items = [item.strip() for item in input_str.split("\n") if item.strip()]
    
    return items

# Action button
st.markdown("---")
col_button1, col_button2 = st.columns([1, 3])

with col_button1:
    run_analysis = st.button(
        "🚀 Run Analysis",
        use_container_width=True,
        type="primary"
    )

with col_button2:
    st.markdown(
        "*This will analyze your waste items for ESG compliance, recyclability, and financial rewards.*"
    )

# Results display
if run_analysis:
    trash_list = parse_trash_list(trash_input)
    
    if not trash_list:
        st.error("❌ Please enter at least one item to analyze.")
    else:
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        with st.spinner("🤖 AI Experts are analyzing your waste..."):
            try:
                result = run_scout_workflow(trash_list)
                
                # Parse result into dictionary
                parsed_result = None
                if isinstance(result, str):
                    try:
                        parsed_result = json.loads(result)
                    except json.JSONDecodeError:
                        st.warning("⚠️ Non-JSON output received")
                        st.info(result)
                        parsed_result = None
                elif isinstance(result, dict):
                    parsed_result = result
                else:
                    try:
                        parsed_result = json.loads(str(result))
                    except:
                        parsed_result = None
                
                # Display results if parsing was successful
                if parsed_result:
                    st.success("✅ Analysis completed successfully!")
                    st.markdown("---")
                    
                    # Handle different result types
                    items_data = []
                    total_reward = 0
                    financial_advice = "No financial advice available"
                    has_finance_task = False
                    
                    # Check if result is combined (has scout_task and finance_task)
                    if isinstance(parsed_result, dict):
                        # Extract scout data
                        if "scout_task" in parsed_result:
                            scout_data = parsed_result.get("scout_task")
                            if isinstance(scout_data, list):
                                items_data = scout_data
                        
                        # Extract finance data
                        if "finance_task" in parsed_result:
                            finance_data = parsed_result.get("finance_task")
                            has_finance_task = True
                            if isinstance(finance_data, dict):
                                # Extract total_reward - handle both numeric and string values
                                reward_value = finance_data.get("total_reward", 0)
                                if isinstance(reward_value, (int, float)):
                                    total_reward = reward_value
                                elif isinstance(reward_value, str):
                                    try:
                                        total_reward = float(reward_value)
                                    except ValueError:
                                        total_reward = 0
                                
                                financial_advice = finance_data.get("Financial Advice", "No financial advice available")
                    
                    # If result is plain list, it's scout_task
                    elif isinstance(parsed_result, list):
                        items_data = parsed_result
                    
                    # Display metrics side-by-side
                    col_metric1, col_metric2, col_metric3 = st.columns(3)
                    with col_metric1:
                        st.metric(label="💰 Total Reward", value=f"${total_reward:.2f}")
                    
                    with col_metric2:
                        st.metric(label="📊 Items Analyzed", value=len(trash_list))
                    
                    with col_metric3:
                        analysis_type = "Multi-Agent (Scout + Finance)" if has_finance_task else "Scout Analysis"
                        st.metric(label="♻️ Analysis Type", value=analysis_type)
                    
                    # Create and display bar chart immediately after metrics
                    st.markdown("---")
                    
                    # Build recyclability chart data
                    if items_data and isinstance(items_data, list) and len(items_data) > 0:
                        try:
                            # Create DataFrame from items data
                            chart_records = []
                            for idx, item in enumerate(items_data):
                                if isinstance(item, dict):
                                    item_name = item.get("item_name", f"Item {idx}")
                                    recyclability_score = item.get("recyclability_score", 0)
                                    
                                    chart_records.append({
                                        "item_name": str(item_name),
                                        "recyclability_score": int(recyclability_score) if isinstance(recyclability_score, (int, float)) else 0
                                    })
                            
                            # Display chart if we have data
                            if chart_records:
                                st.subheader("📈 Recyclability Scores")
                                df_recyclability = pd.DataFrame(chart_records)
                                
                                try:
                                    st.bar_chart(
                                        data=df_recyclability.set_index("item_name")["recyclability_score"],
                                        height=350
                                    )
                                except Exception as chart_error:
                                    st.error(f"❌ Bar chart error: {type(chart_error).__name__}: {str(chart_error)}")
                                    st.bar_chart(df_recyclability.set_index("item_name"))
                                
                                # Show detailed table
                                st.markdown("**Item-by-Item Breakdown:**")
                                st.dataframe(df_recyclability, use_container_width=True, hide_index=True)
                            else:
                                st.warning("⚠️ No valid chart records created")
                        except Exception as e:
                            st.error(f"❌ Chart creation error: {type(e).__name__}")
                            st.error(f"Details: {str(e)}")
                    else:
                        st.info("ℹ️ No recyclability data available for chart")
                    
                    # Financial advice section
                    st.markdown("---")
                    if has_finance_task or financial_advice != "No financial advice available":
                        st.subheader("💡 Financial Advice")
                        st.info(financial_advice)
                    
                    # Detailed analysis in expandable section
                    st.markdown("---")
                    with st.expander("📋 View Detailed Analysis"):
                        st.json(parsed_result)
                    
                    st.markdown("---")
                    st.success("✅ Analysis complete! All results displayed above.")
                else:
                    st.warning("⚠️ Could not parse analysis results. Raw output:")
                    st.json(result if isinstance(result, dict) else str(result))
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.markdown("**Troubleshooting tips:**")
                st.markdown("""
                - Ensure GOOGLE_API_KEY is set in .env file
                - Check internet connection for LLM API access
                - Verify all required packages are installed
                """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    Built for GDGoC Hackathon Vietnam 2026 | Powered by CrewAI + Streamlit
</div>
""", unsafe_allow_html=True)
