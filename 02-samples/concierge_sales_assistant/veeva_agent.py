from strands import Agent, tool
from strands.models import BedrockModel
from constants import SESSION_ID
from dummy_data_subagents import COMPLETE_VEEVA_DATA
import json
from datetime import datetime

model = BedrockModel(
    model_id="arn:aws:bedrock:us-west-2:558178433193:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)

def query_veeva_data(query: str):
    """Query the dummy Veeva engagement data based on the user query."""
    query_lower = query.lower()
    engagements = COMPLETE_VEEVA_DATA['engagements']
    results = []
    
    # Doctor-specific engagement queries
    if any(doc_name in query_lower for doc_name in ['dr. julie', 'dr. shafique', 'dr. sarah', 'dr. smith', 'julie', 'shafique']):
        # Find doctor name in query
        doctor_name = None
        for engagement in engagements:
            if engagement['doctor'].lower() in query_lower or engagement['doctor'].lower().replace('dr. ', '') in query_lower:
                doctor_name = engagement['doctor']
                break
        
        if doctor_name:
            results = [eng for eng in engagements if eng['doctor'] == doctor_name]
            
            # Sort by date descending for "last engagement" queries
            if 'last' in query_lower:
                results = sorted(results, key=lambda x: x['date'], reverse=True)[:1]
            elif 'three' in query_lower or '3' in query_lower:
                results = sorted(results, key=lambda x: x['date'], reverse=True)[:3]
    
    # General engagement queries
    elif any(word in query_lower for word in ['engagement', 'call', 'visit', 'meeting', 'interaction']):
        if 'last month' in query_lower:
            # Mock last month's engagements
            results = engagements  # All engagements as they're recent
        elif 'conversion' in query_lower or 'successful' in query_lower:
            # Filter successful engagements
            results = [eng for eng in engagements if 'positive' in eng['outcome'].lower()]
        else:
            results = engagements
    
    # Talking points queries
    elif any(word in query_lower for word in ['talking points', 'discussion', 'discussed']):
        results = engagements
        
    return results

veeva_agent = Agent(
    model=model,
    system_prompt="""You are a Veeva CRM specialist assistant with access to real physician engagement data including call notes, interaction history, and talking points.
    Analyze the provided engagement data and give specific, actionable responses. Format your responses clearly with engagement details like dates, types, outcomes, and talking points.
    When preparing for calls, provide relevant context from previous interactions and suggest follow-up topics.""",
    trace_attributes={"session.id": SESSION_ID},
)

@tool 
def veeva_assistant(query: str) -> str:
    """Handle Veeva-related queries about physician engagements, call notes, and interaction history."""
    print(f"👥 VEEVA AGENT: Processing engagement query - '{query}'")
    
    # Query the data
    data_results = query_veeva_data(query)
    
    # Prepare context for the agent
    context = f"User Query: {query}\n\nRelevant Veeva Engagement Data:\n{json.dumps(data_results, indent=2)}"
    
    response = veeva_agent(f"Based on this Veeva engagement data, provide a specific answer to the user's query:\n\n{context}")
    return str(response)