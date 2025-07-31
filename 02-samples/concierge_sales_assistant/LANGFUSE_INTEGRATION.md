# Langfuse Observability Integration

This document describes the Langfuse observability integration for the Concierge Sales Assistant.

## Overview

The Concierge Sales Assistant now includes comprehensive observability through Langfuse, providing:
- **Full trace visibility** for multi-agent interactions
- **Session tracking** across all specialized agents
- **Custom tags and attributes** for business context
- **Agent routing analysis** to understand query classification

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Langfuse Credentials
Set your Langfuse credentials as environment variables:

```bash
export LANGFUSE_PUBLIC_KEY="pk_lf_your_public_key"
export LANGFUSE_SECRET_KEY="sk_lf_your_secret_key"
```

Get these keys from your Langfuse project settings: https://cloud.langfuse.com

### 3. Run the Application
```bash
python concierge_sales_assistant.py
```

## Features

### Automatic Trace Collection
- **Main Coordinator**: Traces query classification and routing decisions
- **Sub-Agents**: Individual traces for Salesforce, Tableau, Training, and Veeva agents
- **Tool Usage**: Detailed tracking of agent-as-tool pattern interactions

### Rich Trace Attributes
Each trace includes:
- `session.id`: Consistent session tracking across all agents
- `agent.name`: Specific agent identifier (e.g., "salesforce_agent", "concierge_coordinator")
- `agent.type`: Always "concierge_sales_assistant"
- `business.domain`: "pharmaceutical_sales"
- `business.company`: "guardant_health"

### Langfuse Tags
- `Concierge-Sales-Assistant`: Main application tag
- `Multi-Agent-System`: System architecture identifier
- `Guardant-Health`: Company identifier
- Agent-specific tags: `Salesforce-Agent`, `Tableau-Agent`, etc.

## Testing Integration

### Quick Test
```bash
python test_langfuse_integration.py
```

This runs sample queries and verifies trace collection.

### Manual Testing
1. Run the main application: `python concierge_sales_assistant.py`
2. Ask various queries to test different routing patterns
3. Check your Langfuse dashboard for traces

## Dashboard Analysis

### Finding Your Traces
1. Go to https://cloud.langfuse.com
2. Navigate to your project
3. Filter by tag: `Concierge-Sales-Assistant`
4. Look for session groupings using the `session.id`

### Multi-Agent Analysis
- **Single-domain queries**: Should show one main trace + one sub-agent trace
- **Multi-domain queries**: Should show one main trace + multiple sub-agent traces
- **Agent routing**: Look at tool usage within main coordinator trace

### Key Metrics to Monitor
- **Query Classification Accuracy**: Are queries routed to correct agents?
- **Response Quality**: Use trace data for evaluation pipeline
- **Performance**: Track response times across agents
- **Usage Patterns**: Understand which agents are used most frequently

## Architecture

The integration follows this pattern:

```
Main Coordinator Agent (concierge_coordinator)
├── Trace Attributes: session.id, business context
├── Tool: salesforce_assistant()
│   └── Sub-Agent Trace (salesforce_agent)
├── Tool: tableau_assistant()
│   └── Sub-Agent Trace (tableau_agent)
├── Tool: training_assistant()
│   └── Sub-Agent Trace (training_agent)
└── Tool: veeva_assistant()
    └── Sub-Agent Trace (veeva_agent)
```

## Configuration Module

The `langfuse_config.py` module provides:
- `setup_langfuse_env()`: Configures OTEL endpoints for Strands integration
- `get_coordinator_trace_attributes()`: Attributes for main coordinator
- `get_subagent_trace_attributes()`: Attributes for specialized agents

## Troubleshooting

### No Traces Appearing
1. Verify credentials are set correctly
2. Check network connectivity to Langfuse
3. Look for error messages in console output
4. Ensure `OTEL_EXPORTER_OTLP_*` environment variables are set

### Incomplete Traces
1. Verify all agents are updated with new trace attributes
2. Check that `langfuse_config` import is working
3. Ensure consistent `SESSION_ID` usage across agents

### Permission Issues
1. Verify your Langfuse project permissions
2. Check that your API keys have correct scope
3. Ensure you're using the correct Langfuse host (US vs EU)

## Future Enhancements

This integration provides the foundation for:
- **Automated Evaluation**: Use traces for quality assessment
- **Performance Monitoring**: Track agent effectiveness over time
- **Business Analytics**: Understand query patterns and user needs
- **A/B Testing**: Compare different routing strategies