import os
from strands import Agent, tool
from strands.models import BedrockModel
from constants import SESSION_ID

aws_account_id = os.environ["AWS_ACCOUNT_ID"]

model = BedrockModel(
    model_id=f"arn:aws:bedrock:us-west-2:{aws_account_id}:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)

# Mock training knowledge base
TRAINING_KNOWLEDGE = {
    "guardant360": {
        "sample_volume": "10mL of blood in EDTA tubes",
        "turnaround_time": "7-14 business days",
        "test_type": "Comprehensive genomic profiling for solid tumors",
        "key_features": ["74 genes analyzed", "TMB and MSI assessment", "FDA approved CDx"],
        "clinical_utility": "Treatment selection and monitoring for advanced solid tumors"
    },
    "guardant_reveal": {
        "sample_volume": "10mL of blood in EDTA tubes", 
        "turnaround_time": "7-10 business days",
        "test_type": "Early detection blood test for colorectal cancer",
        "key_features": ["Detects colorectal cancer and pre-cancer", "Non-invasive screening", "Methylation-based assay"],
        "draw_guidelines": "Draw date must be within 30 days of physician order"
    },
    "kit_shortage_procedure": {
        "immediate_actions": [
            "Contact Territory Manager immediately",
            "Check alternative shipping locations",
            "Offer expedited shipping for urgent cases",
            "Provide ETA for kit replenishment"
        ],
        "escalation": "If urgent patient need, contact Customer Service at 1-800-xxx-xxxx",
        "communication": "Proactively inform affected physicians about timeline"
    },
    "ops_scheduling": {
        "guidelines": [
            "Schedule OPS draws within 72 hours of order placement",
            "Confirm patient availability and fasting requirements",
            "Ensure proper kit selection for test type",
            "Verify insurance authorization if required"
        ],
        "best_practices": "Coordinate with physician office to minimize patient wait times"
    },
    "billing_responsibilities": {
        "patient_responsibility": [
            "Patient copays and deductibles apply",
            "Uninsured patients may qualify for financial assistance",
            "Patient should be informed of potential costs upfront"
        ],
        "physician_responsibility": [
            "Verify insurance coverage before ordering",
            "Obtain prior authorization when required",
            "Complete accurate diagnostic coding"
        ]
    }
}

def query_training_data(query: str):
    """Query the mock training knowledge base."""
    query_lower = query.lower()
    results = {}
    
    # Product-specific queries
    if 'guardant360' in query_lower:
        if 'sample' in query_lower or 'volume' in query_lower:
            results = {"product": "Guardant360", "info": TRAINING_KNOWLEDGE["guardant360"]}
        else:
            results = {"product": "Guardant360", "info": TRAINING_KNOWLEDGE["guardant360"]}
    
    elif 'reveal' in query_lower:
        if 'draw' in query_lower or 'guidelines' in query_lower:
            results = {"product": "Guardant Reveal", "info": TRAINING_KNOWLEDGE["guardant_reveal"]}
        else:
            results = {"product": "Guardant Reveal", "info": TRAINING_KNOWLEDGE["guardant_reveal"]}
    
    # Procedural queries
    elif 'kit' in query_lower and ('out' in query_lower or 'shortage' in query_lower):
        results = {"procedure": "Kit Shortage", "info": TRAINING_KNOWLEDGE["kit_shortage_procedure"]}
    
    elif 'ops' in query_lower and 'scheduling' in query_lower:
        results = {"procedure": "OPS Scheduling", "info": TRAINING_KNOWLEDGE["ops_scheduling"]}
    
    elif 'billing' in query_lower or 'patient billing' in query_lower:
        results = {"procedure": "Patient Billing", "info": TRAINING_KNOWLEDGE["billing_responsibilities"]}
    
    # General training queries
    elif any(word in query_lower for word in ['training', 'materials', 'latest', 'recent']):
        results = {
            "latest_materials": [
                "Q1 2024 Product Update Training (Released Jan 15, 2024)",
                "New Reimbursement Guidelines Webinar (Released Jan 8, 2024)", 
                "Customer Objection Handling Refresher (Released Dec 20, 2023)",
                "Guardant Reveal Clinical Evidence Update (Released Jan 3, 2024)"
            ]
        }
    
    return results

training_agent = Agent(
    model=model,
    system_prompt="""You are a sales training and knowledge base specialist assistant with access to comprehensive product information, clinical guidelines, and procedural documentation for Guardant Health products.
    Provide specific, accurate information from the training knowledge base. Format your responses clearly with relevant details like sample requirements, procedures, and best practices.
    When providing training information, be precise about specifications, timelines, and compliance requirements.""",
    trace_attributes={"session.id": SESSION_ID},
)

@tool
def training_assistant(query: str) -> str:
    """Handle training and knowledge base queries about products, guidelines, procedures, and best practices."""
    print(f"📚 TRAINING AGENT: Processing knowledge query - '{query}'")
    
    # Query the knowledge base
    knowledge_results = query_training_data(query)
    
    if knowledge_results:
        import json
        context = f"User Query: {query}\n\nRelevant Training Knowledge:\n{json.dumps(knowledge_results, indent=2)}"
        response = training_agent(f"Based on this training knowledge, provide a specific and detailed answer to the user's query:\n\n{context}")
    else:
        # Fallback for queries not in knowledge base
        response = training_agent(f"This query is about training/knowledge: {query}. Provide helpful guidance based on general sales training best practices for medical diagnostics.")
    
    return str(response)