#!/usr/bin/env python3
"""
Test the main concierge application with a single query to verify tracing.
"""

import os
import time
from strands import Agent
from strands.models import BedrockModel
from salesforce_agent import salesforce_assistant
from tableau_agent import tableau_assistant  
from training_agent import training_assistant
from veeva_agent import veeva_assistant
from constants import SESSION_ID
from langfuse_config import setup_langfuse_env, get_coordinator_trace_attributes

# Show rich UI for tools in CLI
os.environ["STRANDS_TOOL_CONSOLE_MODE"] = "enabled"

# Setup Langfuse observability
print("🔧 Configuring Langfuse observability...")
setup_langfuse_env()
print("✅ Langfuse configuration complete!")
print()

aws_account_id = os.environ["AWS_ACCOUNT_ID"]

model = BedrockModel(
    model_id=f"arn:aws:bedrock:us-west-2:{aws_account_id}:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)

system_prompt = """You are a Concierge Sales Assistant for sales representatives at Guardant Health. You intelligently classify queries and route them to the appropriate specialized agents.

IMPORTANT: For each query, automatically determine which categories apply and use the corresponding assistant tools:

**CATEGORIES:**
- **sales_training_related**: Product specs, procedures, guidelines, best practices, compliance, training materials
- **salesforce_related**: CRM data, cases, samples, accounts, territories, support tickets, physician/patient info
- **tableau_related**: Analytics, quotas, performance metrics, revenue tracking, territory analysis, forecasting
- **veeva_related**: Physician engagements, call notes, interaction history, relationship tracking

**ROUTING RULES:**
- Use training_assistant() for sales_training_related queries
- Use salesforce_assistant() for salesforce_related queries  
- Use tableau_assistant() for tableau_related queries
- Use veeva_assistant() for veeva_related queries

You are the intelligent coordinator that ensures sales reps get complete, accurate information from all relevant systems."""

print("🤖 Creating Concierge Sales Agent...")
concierge_sales_agent = Agent(
    model=model,
    system_prompt=system_prompt,
    tools=[salesforce_assistant, tableau_assistant, training_assistant, veeva_assistant],
    trace_attributes=get_coordinator_trace_attributes(SESSION_ID),
)
print("✅ Agent created with trace attributes!")
print(f"   Session ID: {SESSION_ID[:50]}...")
print()

# Test with a simple query
test_query = "Show me open cases in my territory"
print(f"🧪 Testing query: '{test_query}'")
print("🤖 Response: ", end="")

start_time = time.time()
try:
    response = concierge_sales_agent(test_query)
    end_time = time.time()
    
    print(f"\n✅ Query completed in {end_time - start_time:.2f} seconds")
    print()
    print("📊 Trace Information:")
    print(f"   Service: concierge-sales-assistant")
    print(f"   Session: {SESSION_ID}")
    print(f"   Query: {test_query}")
    print(f"   Duration: {end_time - start_time:.2f}s")
    print()
    print("🔍 Check your Langfuse dashboard:")
    print("   URL: https://us.cloud.langfuse.com")
    print("   Look for traces with:")
    print(f"   - Service: concierge-sales-assistant")
    print(f"   - Session ID: {SESSION_ID}")
    print(f"   - Tags: Concierge-Sales-Assistant, Multi-Agent-System")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("This error might still generate traces showing the failure.")

print()
print("⏱️  Traces should appear in Langfuse within 1-2 minutes.")
print("🔄 If no traces appear, check your API keys and project settings.")