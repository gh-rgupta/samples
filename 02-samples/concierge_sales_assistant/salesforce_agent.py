from strands import Agent, tool
from strands.models import BedrockModel
from constants import SESSION_ID
from dummy_data_subagents import COMPLETE_SALESFORCE_DATA
import json
from datetime import datetime, timedelta

model = BedrockModel(
    model_id="arn:aws:bedrock:us-west-2:558178433193:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)

def query_salesforce_data(query: str):
    """Query the dummy Salesforce data based on the user query."""
    query_lower = query.lower()
    results = []
    
    # Orders queries
    if any(word in query_lower for word in ['orders', 'cases', 'samples', 'processing', 'hold', 'received']):
        orders = COMPLETE_SALESFORCE_DATA['orders']
        
        if 'hold' in query_lower or 'on hold' in query_lower:
            results = [order for order in orders if order['status'].lower() == 'on hold']
            
        elif 'processing' in query_lower:
            results = [order for order in orders if order['status'].lower() == 'processing']
            
        elif 'received' in query_lower or 'yesterday' in query_lower:
            # Mock yesterday's received samples
            results = [order for order in orders if order['status'].lower() == 'completed'][:3]
            
        elif 'cancelled' in query_lower:
            results = [order for order in orders if order['status'].lower() == 'cancelled']
            
        elif 'dr. shafique' in query_lower or 'shafique' in query_lower:
            results = [order for order in orders if 'shafique' in order['doctor'].lower()]
            
        else:
            # Return recent active orders
            results = [order for order in orders if order['status'] in ['On Hold', 'Processing', 'Completed']][:5]
    
    # Stark compliance queries
    elif any(word in query_lower for word in ['stark', 'limit', 'compliance', 'nearing']):
        stark_data = COMPLETE_SALESFORCE_DATA['stark_compliance']
        
        if 'nearing' in query_lower:
            results = [doc for doc in stark_data if doc['risk_level'] == 'High' or doc['percentage_used'] > 70]
        else:
            results = stark_data
    
    # Doctor-specific queries
    elif any(doc_name in query_lower for doc_name in ['dr.', 'doctor', 'physician']):
        orders = COMPLETE_SALESFORCE_DATA['orders']
        stark = COMPLETE_SALESFORCE_DATA['stark_compliance']
        
        # Find doctor name in query
        doctor_name = None
        for order in orders:
            if order['doctor'].lower() in query_lower:
                doctor_name = order['doctor']
                break
        
        if doctor_name:
            doctor_orders = [order for order in orders if order['doctor'] == doctor_name]
            doctor_stark = [doc for doc in stark if doc['doctor'] == doctor_name]
            results = {'orders': doctor_orders, 'stark_compliance': doctor_stark}
    
    return results

salesforce_agent = Agent(
    model=model,
    system_prompt="""You are a Salesforce specialist assistant with access to real CRM data including orders, cases, samples, and Stark compliance information. 
    Analyze the provided data and give specific, actionable responses. Format your responses clearly with relevant details like order IDs, dates, amounts, and status information.
    When presenting data, use clear formatting and highlight important information like high-risk Stark compliance or urgent cases.""",
    trace_attributes={"session.id": SESSION_ID},
)

@tool
def salesforce_assistant(query: str) -> str:
    """Handle Salesforce-related queries about cases, samples, accounts, territories, and support tickets."""
    print(f"🔵 SALESFORCE AGENT: Processing query - '{query}'")
    
    # Query the data
    data_results = query_salesforce_data(query)
    
    # Prepare context for the agent
    context = f"User Query: {query}\n\nRelevant Salesforce Data:\n{json.dumps(data_results, indent=2)}"
    
    response = salesforce_agent(f"Based on this Salesforce data, provide a specific answer to the user's query:\n\n{context}")
    return str(response)