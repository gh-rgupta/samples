#!/usr/bin/env python3
"""
Debug script to test Langfuse tracing with Strands Agents.
"""

import os
from strands import Agent
from strands.models import BedrockModel
from constants import SESSION_ID
from langfuse_config import setup_langfuse_env, get_coordinator_trace_attributes

# Set up environment variables
export_commands = """
export LANGFUSE_PUBLIC_KEY="pk-lf-1d537221-c3d2-4b1f-8a42-2de2601de53d"
export LANGFUSE_SECRET_KEY="sk-lf-357ab81a-dc5d-4736-948e-cdcf0a54783a"
export LANGFUSE_HOST="https://us.cloud.langfuse.com"
"""

print("Make sure you've run these commands:")
print(export_commands)
print()

# Setup Langfuse observability
print("🔧 Setting up Langfuse observability...")
setup_langfuse_env()
print()

# Setup AWS account (you need to set this)
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
if not aws_account_id:
    print("❌ AWS_ACCOUNT_ID environment variable not set!")
    print("Please run: export AWS_ACCOUNT_ID=your_account_id")
    exit(1)

print(f"✅ AWS Account ID: {aws_account_id}")
print(f"✅ Session ID: {SESSION_ID}")
print()

# Create a simple model
model = BedrockModel(
    model_id=f"arn:aws:bedrock:us-west-2:{aws_account_id}:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)

# Create a simple agent with tracing
print("🤖 Creating agent with tracing...")
simple_agent = Agent(
    model=model,
    system_prompt="You are a helpful assistant. Always respond cheerfully and briefly.",
    trace_attributes=get_coordinator_trace_attributes(SESSION_ID),
)

print("✅ Agent created with trace attributes!")
print()

# Test a simple interaction
print("🧪 Testing agent interaction...")
try:
    print("User: Hello, can you help me?")
    response = simple_agent("Hello, can you help me?")
    print(f"Agent: {response}")
    print()
    print("✅ Test interaction completed!")
    print()
    print("📊 Check your Langfuse dashboard at: https://us.cloud.langfuse.com")
    print("   Look for traces from service: concierge-sales-assistant")

except Exception as e:
    print(f"❌ Error during interaction: {e}")
    print("This might indicate a tracing configuration issue.")

print()
print("🔍 Environment check:")
print(f"   OTEL_EXPORTER_OTLP_ENDPOINT: {os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', 'Not set')}")
print(f"   OTEL_TRACES_EXPORTER: {os.environ.get('OTEL_TRACES_EXPORTER', 'Not set')}")
print(f"   OTEL_SERVICE_NAME: {os.environ.get('OTEL_SERVICE_NAME', 'Not set')}")