import os
import time
from strands import Agent
from strands.models import BedrockModel
from salesforce_agent import salesforce_assistant as _salesforce_assistant
from tableau_agent import tableau_assistant as _tableau_assistant  
from training_agent import training_assistant as _training_assistant
from veeva_agent import veeva_assistant as _veeva_assistant
from strands import tool
from constants import SESSION_ID
from langfuse_config import setup_langfuse_env, get_coordinator_trace_attributes

# Show rich UI for tools in CLI
os.environ["STRANDS_TOOL_CONSOLE_MODE"] = "enabled"

# Global variable to store agent execution times
agent_execution_times = {}

# Timing wrapper functions for each agent
@tool
def salesforce_assistant(query: str) -> str:
    """Handle Salesforce-related queries about cases, samples, accounts, territories, and support tickets."""
    start_time = time.time()
    print(f"⏱️  [TIMING] Salesforce Agent - Starting query execution...")
    
    result = _salesforce_assistant(query)
    
    end_time = time.time()
    execution_time = end_time - start_time
    agent_execution_times['salesforce'] = execution_time
    print(f"⏱️  [TIMING] Salesforce Agent - Completed in {execution_time:.2f} seconds")
    
    return result

@tool
def tableau_assistant(query: str) -> str:
    """Handle Tableau-related queries about analytics, quotas, performance metrics, and revenue tracking."""
    start_time = time.time()
    print(f"⏱️  [TIMING] Tableau Agent - Starting query execution...")
    
    result = _tableau_assistant(query)
    
    end_time = time.time()
    execution_time = end_time - start_time
    agent_execution_times['tableau'] = execution_time
    print(f"⏱️  [TIMING] Tableau Agent - Completed in {execution_time:.2f} seconds")
    
    return result

@tool
def training_assistant(query: str) -> str:
    """Handle training-related queries about product specs, procedures, guidelines, and best practices."""
    start_time = time.time()
    print(f"⏱️  [TIMING] Training Agent - Starting query execution...")
    
    result = _training_assistant(query)
    
    end_time = time.time()
    execution_time = end_time - start_time
    agent_execution_times['training'] = execution_time
    print(f"⏱️  [TIMING] Training Agent - Completed in {execution_time:.2f} seconds")
    
    return result

@tool
def veeva_assistant(query: str) -> str:
    """Handle Veeva-related queries about physician engagements, call notes, and interaction history."""
    start_time = time.time()
    print(f"⏱️  [TIMING] Veeva Agent - Starting query execution...")
    
    result = _veeva_assistant(query)
    
    end_time = time.time()
    execution_time = end_time - start_time
    agent_execution_times['veeva'] = execution_time
    print(f"⏱️  [TIMING] Veeva Agent - Completed in {execution_time:.2f} seconds")
    
    return result

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

**FOR COMPLEX QUERIES:**
If a query spans multiple categories, call multiple assistants and synthesize their responses. Examples:

Query: "Show me current reveal cases and corresponding draw date guidelines"
→ Call salesforce_assistant() for cases + training_assistant() for guidelines

Query: "Who are my top 5 contacts with highest engagements and what tests do they order?"
→ Call tableau_assistant() for top contacts + salesforce_assistant() for test orders

Query: "What should I know before my call with Dr. Shafique?"
→ Call salesforce_assistant() for case updates + veeva_assistant() for past engagements + training_assistant() for relevant materials

**RESPONSE STYLE:**
- Keep responses SHORT and CONCISE
- Use bullet points and structured format
- Avoid lengthy explanations
- Focus on actionable information
- Maximum 3-4 sentences per point
- Use clear, direct language

**YOUR APPROACH:**
1. Analyze the query to identify which categories apply
2. Call the appropriate assistant tool(s)
3. If multiple tools are used, synthesize the responses into a brief, structured answer
4. Provide concise, actionable information without unnecessary detail

You are the intelligent coordinator that ensures sales reps get complete, accurate information from all relevant systems in a brief, digestible format."""

concierge_sales_agent = Agent(
    model=model,
    system_prompt=system_prompt,
    tools=[salesforce_assistant, tableau_assistant, training_assistant, veeva_assistant],
    trace_attributes=get_coordinator_trace_attributes(SESSION_ID),
)

if __name__ == "__main__":
    print("=============================================================================")
    print("🏢  WELCOME TO YOUR CONCIERGE SALES ASSISTANT  🏢")
    print("=============================================================================")
    print("✨ I'm your intelligent sales coordinator with access to:")
    print("   🔵 Salesforce Assistant - Cases, samples, accounts, territories")
    print("   📊 Tableau Assistant - Analytics, quotas, performance metrics")
    print("   📚 Training Assistant - Product specs, guidelines, procedures")
    print("   👥 Veeva Assistant - Physician engagements and call notes")
    print()
    print("🎯 I automatically route your queries to the right systems:")
    print("   • 'Show me open cases in my territory' → Salesforce")
    print("   • 'How am I tracking against quota?' → Tableau")
    print("   • 'What are Guardant360 sample requirements?' → Training")
    print("   • 'When did I last engage Dr. Smith?' → Veeva")
    print("   • Complex queries → Multiple systems combined!")
    print()
    print("💡 Just ask me anything - I'll get the right information!")
    print("🚪 Type 'exit' to quit anytime")
    print("=============================================================================")
    print()

    # Initialize the concierge sales assistant
    try:
        print("🔄 Initializing Concierge Sales Assistant...")
        print("✅ Concierge Sales Assistant ready!")
        print("🤖 All specialized agents are available!")
        print()
    except Exception as e:
        print(f"❌ Error initializing Concierge Sales Assistant: {str(e)}")

    # Run the agent in a loop for interactive conversation
    while True:
        try:
            user_input = input("👤 You: ").strip()
            if not user_input:
                print("💭 Please ask me about cases, analytics, training, or engagements - or type 'exit' to quit")
                continue
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                print()
                print("=========================================================")
                print("👋 Thank you for using Concierge Sales Assistant!")
                print("📈 Keep selling and stay informed!")
                print("🤖 Come back anytime you need sales support!")
                print("=========================================================")
                break

            # Reset agent execution times for new query
            agent_execution_times.clear()
            
            # Start total query timing
            total_start_time = time.time()
            print("⏱️  [TIMING] Total Query - Starting execution...")
            print()
            
            print("🤖 ConciergeBot: ", end="")
            response = concierge_sales_agent(user_input)
            
            # End total query timing
            total_end_time = time.time()
            total_execution_time = total_end_time - total_start_time
            
            print()
            print("=" * 60)
            print("⏱️  [TIMING SUMMARY]")
            print("=" * 60)
            
            # Show individual agent times
            if agent_execution_times:
                for agent_name, execution_time in agent_execution_times.items():
                    print(f"   📊 {agent_name.capitalize()} Agent: {execution_time:.2f} seconds")
                print("   " + "-" * 40)
                sub_agent_total = sum(agent_execution_times.values())
                print(f"   📊 Sub-agents Total: {sub_agent_total:.2f} seconds")
                coordinator_time = total_execution_time - sub_agent_total
                print(f"   🤖 Coordinator Overhead: {coordinator_time:.2f} seconds")
            else:
                print("   📊 No sub-agents were called for this query")
            
            print(f"   ⏱️  Total Query Time: {total_execution_time:.2f} seconds")
            print("=" * 60)
            print()

        except KeyboardInterrupt:
            print("\n")
            print("=========================================================")
            print("👋 Concierge Sales Assistant interrupted!")
            print("🤖 See you next time!")
            print("=========================================================")
            break
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")
            print("🔧 Please try again or type 'exit' to quit")
            print()