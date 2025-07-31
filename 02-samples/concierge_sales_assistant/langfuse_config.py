"""
Langfuse configuration module for the Concierge Sales Assistant.
Sets up observability and tracing for the multi-agent system.
"""

import os
import base64
from typing import Optional

def setup_langfuse_env(
    public_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    host: str = "https://us.cloud.langfuse.com"
) -> None:
    """
    Configure environment variables for Langfuse integration with Strands Agents.
    
    Args:
        public_key: Langfuse public key (if not provided, uses LANGFUSE_PUBLIC_KEY env var)
        secret_key: Langfuse secret key (if not provided, uses LANGFUSE_SECRET_KEY env var)
        host: Langfuse host URL (defaults to US cloud)
    """
    # HARDCODED CREDENTIALS FOR TESTING - Remove in production!
    HARDCODED_PUBLIC_KEY = "pk-lf-1d537221-c3d2-4b1f-8a42-2de2601de53d"
    HARDCODED_SECRET_KEY = "sk-lf-357ab81a-dc5d-4736-948e-cdcf0a54783a"
    HARDCODED_HOST = "https://us.cloud.langfuse.com"
    
    # Use hardcoded values first, then parameters, then environment variables
    host = HARDCODED_HOST
    pub_key = HARDCODED_PUBLIC_KEY  
    sec_key = HARDCODED_SECRET_KEY
    
    # Override with parameters if provided
    if public_key:
        pub_key = public_key
    if secret_key:
        sec_key = secret_key
    
    # Set environment variables so they're available
    os.environ["LANGFUSE_HOST"] = host
    os.environ["LANGFUSE_PUBLIC_KEY"] = pub_key
    os.environ["LANGFUSE_SECRET_KEY"] = sec_key
    
    if not pub_key or not sec_key:
        print("⚠️  Langfuse keys not found. Please set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY environment variables.")
        print("   You can get these from: https://cloud.langfuse.com (project settings)")
        return
    
    # Set Langfuse host
    
    
    # Set up OTEL endpoint for Strands Agents integration
    otel_endpoint = f"{host}/api/public/otel/v1/traces"
    
    # Create authentication token
    auth_token = base64.b64encode(f"{pub_key}:{sec_key}".encode()).decode()
    
    # Configure OTEL environment variables for Strands Agents
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = otel_endpoint
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_token}"
    
    # Enable tracing
    os.environ["OTEL_TRACES_EXPORTER"] = "otlp"
    os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "http/protobuf"
    os.environ["OTEL_SERVICE_NAME"] = "concierge-sales-assistant"
    os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "service.name=concierge-sales-assistant,service.version=1.0.0"
    
    # Additional OTEL settings for better trace export
    os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = otel_endpoint
    os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"] = f"Authorization=Basic {auth_token}"
    os.environ["OTEL_EXPORTER_OTLP_TRACES_PROTOCOL"] = "http/protobuf"
    
    # Force immediate export for testing
    os.environ["OTEL_BSP_SCHEDULE_DELAY"] = "1000"  # 1 second delay
    os.environ["OTEL_BSP_MAX_EXPORT_BATCH_SIZE"] = "1"  # Export immediately
    
    print(f"✅ Langfuse observability configured for {host}")
    print(f"   Traces will be sent to: {otel_endpoint}")
    print(f"   Service: {os.environ['OTEL_SERVICE_NAME']}")
    print(f"   Protocol: {os.environ['OTEL_EXPORTER_OTLP_PROTOCOL']}")

def get_trace_attributes(agent_name: str, session_id: str, user_id: str = "concierge-user") -> dict:
    """
    Generate standard trace attributes for the multi-agent system.
    
    Args:
        agent_name: Name of the agent (e.g., "concierge_coordinator", "salesforce_agent")
        session_id: Session identifier for tracking conversations
        user_id: User identifier
        
    Returns:
        Dictionary of trace attributes for Strands Agent
    """
    return {
        "session.id": session_id,
        "user.id": user_id,
        "agent.name": agent_name,
        "agent.type": "concierge_sales_assistant",
        "langfuse.tags": [
            "Concierge-Sales-Assistant",
            "Multi-Agent-System", 
            "Guardant-Health",
            agent_name.replace("_", "-").title()
        ],
        "business.domain": "pharmaceutical_sales",
        "business.company": "guardant_health"
    }

def get_coordinator_trace_attributes(session_id: str, user_id: str = "concierge-user") -> dict:
    """Get trace attributes for the main coordinator agent."""
    return get_trace_attributes("concierge_coordinator", session_id, user_id)

def get_subagent_trace_attributes(agent_name: str, session_id: str, user_id: str = "concierge-user") -> dict:
    """Get trace attributes for sub-agents."""
    return get_trace_attributes(f"{agent_name}_agent", session_id, user_id)