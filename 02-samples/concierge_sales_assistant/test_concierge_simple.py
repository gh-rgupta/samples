#!/usr/bin/env python3
"""
Simple test of the main concierge application with hardcoded credentials.
"""

import os
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

print("🏢 CONCIERGE SALES ASSISTANT - TRACE TEST")
print("=" * 50)

# Setup Langfuse observability with hardcoded credentials
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
"""

print("🤖 Creating Concierge Sales Agent...")
concierge_sales_agent = Agent(
    model=model,
    system_prompt=system_prompt,
    tools=[salesforce_assistant, tableau_assistant, training_assistant, veeva_assistant],
    trace_attributes=get_coordinator_trace_attributes(SESSION_ID),
)
print("✅ Agent created with trace attributes!")
print(f"   Session ID: {SESSION_ID}")
print()

# Test with a simple query that should route to Salesforce
test_query = "Show me open cases in my territory"
print(f"🧪 Testing query: '{test_query}'")
print("   Expected: Should route to Salesforce agent")
print()
print("🤖 ConciergeBot: ", end="")

try:
    response = concierge_sales_agent(test_query)
    print("\n✅ Query completed successfully!")
    print()
    print("📊 Trace Information:")
    print(f"   Service: concierge-sales-assistant")
    print(f"   Session: {SESSION_ID}")
    print(f"   Query: {test_query}")
    print("   Expected traces:")
    print("   - Main coordinator agent interaction")
    print("   - Tool call to salesforce_assistant")
    print("   - Salesforce agent response")
    print()
    print("🔍 Check your Langfuse dashboard:")
    print("   URL: https://us.cloud.langfuse.com")
    print("   Look for:")
    print("   - Service: concierge-sales-assistant")
    print(f"   - Session ID: {SESSION_ID}")
    print("   - Tags: Concierge-Sales-Assistant, Multi-Agent-System")
    print("   - Tool usage traces showing salesforce_assistant call")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Even if there's an error, traces should still be generated")

print()
print("⏱️  Traces should appear in Langfuse within 1-2 minutes.")
print("🎯 Success indicators:")
print("   ✅ Direct Langfuse SDK traces (from our earlier tests)")
print("   ✅ OTEL traces from Strands Agent (multi-agent system)")
print("   ✅ Tool usage traces (coordinator → sub-agents)")
print("   ✅ Session continuity across agent interactions")