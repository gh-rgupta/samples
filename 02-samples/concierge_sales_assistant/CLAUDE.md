# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Concierge Sales Assistant built with Strands Agents using a multi-agent architecture. The system demonstrates intelligent query classification and routing where a master coordinator automatically directs sales queries to specialized agents across different data sources: Salesforce CRM, Tableau Analytics, Sales Training Knowledge Base, and Veeva Engagement Tracking.

## Development Commands

### Running the Application
```bash
# Main Concierge Sales Assistant (multi-agent coordinator)
python -u concierge_sales_assistant.py

# Individual Agent Testing
python -u salesforce_agent.py
python -u tableau_agent.py  
python -u training_agent.py
python -u veeva_agent.py
```

### Setup Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Configure AWS credentials for Bedrock
aws configure
# OR export environment variables:
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-west-2
```

## Architecture

### Multi-Agent System
The project implements a master-coordinator pattern with the main agent (`concierge_sales_assistant.py`) intelligently routing queries to four specialized agents:

- **Salesforce Agent** (`salesforce_agent.py`): CRM data, cases, samples, accounts, territories, support tickets
- **Tableau Agent** (`tableau_agent.py`): Analytics, quotas, performance metrics, revenue tracking, forecasting  
- **Training Agent** (`training_agent.py`): Product specs, procedures, guidelines, best practices, compliance materials
- **Veeva Agent** (`veeva_agent.py`): Physician engagements, call notes, interaction history, relationship tracking

### Intelligent Query Classification
The master coordinator uses a sophisticated system prompt that automatically:
1. **Classifies** queries into categories (sales_training_related, salesforce_related, tableau_related, veeva_related)
2. **Routes** to appropriate specialized agents using agent-as-tools pattern
3. **Synthesizes** responses from multiple agents for complex composite queries
4. **Handles** single-domain and multi-domain queries seamlessly

### Agent-as-Tool Pattern
Each specialized agent is exposed as a `@tool` decorated function:

```python
@tool
def salesforce_assistant(query: str) -> str:
    """Handle Salesforce-related queries about cases, samples, accounts, territories, and support tickets."""
    response = salesforce_agent(query)
    return str(response)
```

### Model Configuration
All agents use AWS Bedrock with Claude Sonnet 4 via specific inference profile ARNs. The model configuration is consistent across agents for unified behavior.

## Key Features

### Query Timing and Performance Monitoring
The system includes comprehensive timing functionality to track performance:
- **Individual Agent Timing**: Each sub-agent execution is timed and reported
- **Total Query Timing**: Complete end-to-end query processing time
- **Coordinator Overhead**: Time spent in routing and coordination logic
- **Timing Summary**: Detailed breakdown displayed after each query with visual timing summary

Example timing output:
```
============================================================
⏱️  [TIMING SUMMARY]
============================================================
   📊 Salesforce Agent: 1.23 seconds
   📊 Training Agent: 0.87 seconds
   ----------------------------------------
   📊 Sub-agents Total: 2.10 seconds
   🤖 Coordinator Overhead: 0.15 seconds
   ⏱️  Total Query Time: 2.25 seconds
============================================================
```

### Automatic Query Classification
The system automatically determines query categories without requiring explicit classification:
- **Single domain**: "Show me open cases" → Routes to Salesforce Agent
- **Multi domain**: "Show me current reveal cases and draw date guidelines" → Routes to both Salesforce + Training Agents
- **Complex composite**: "What should I know before my call with Dr. Shafique?" → Routes to Salesforce + Veeva + Training Agents

### Placeholder Implementation
Currently, all specialized agents are placeholder implementations that:
- Print descriptive output showing what data sources they would access
- Use the actual Strands Agent framework to acknowledge queries
- Demonstrate the routing and coordination patterns
- Can be easily replaced with real data source integrations

### Benchmark Testing
Includes comprehensive benchmark dataset (`benchmark_questions.py`) with 32 real-world sales queries covering:
- Single-domain queries for each agent type
- Multi-domain composite queries requiring coordination
- Complex scenarios spanning 3+ systems

## Development Notes

### Interactive Loop Pattern
The main coordinator follows the personal assistant structure:
- Rich welcome message with capability overview
- Input loop with graceful exit handling ("exit", "quit", "bye", "goodbye")
- Exception handling for KeyboardInterrupt and runtime errors
- Consistent emoji-based UI patterns for better user experience

### Environment Configuration
- `STRANDS_TOOL_CONSOLE_MODE="enabled"` enables rich UI for tools
- All agents share the same `SESSION_ID` from `constants.py` for tracing continuity
- Placeholder agents print diagnostic information for development visibility

### Error Handling Patterns
Each agent implements comprehensive error handling for initialization failures, runtime exceptions, and user interrupts with informative error messages and recovery suggestions.

### Query Examples by Category

**Training Queries:**
- "What is the minimum sample volume required for Guardant360 testing?"
- "How should I handle a situation where a physician is out of kits?"

**Salesforce Queries:**
- "Show me the open report hold cases in my territory"
- "Which patients have OPS draws scheduled today?"

**Tableau Queries:**
- "How am I tracking against my monthly sales quota?"
- "Who are the top 5 performers in my territory by revenue?"

**Veeva Queries:**
- "When and who had the last engagement with Dr. Julie Kish?"
- "What were the main talking points in my last three calls with Dr. David?"

**Composite Queries:**
- "Show me current reveal cases and corresponding draw date guidelines" (Salesforce + Training)
- "Who are my top 5 contacts with highest engagements and what tests do they order?" (Tableau + Salesforce)
- "What should I know before my call with Dr. Shafique?" (Salesforce + Veeva + Training)