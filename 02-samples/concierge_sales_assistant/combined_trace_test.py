#!/usr/bin/env python3
"""
Combined test - Direct Langfuse SDK + Strands Agent tracing with hardcoded credentials.
"""

import os
from langfuse import Langfuse
from strands import Agent
from strands.models import BedrockModel
from constants import SESSION_ID
from langfuse_config import setup_langfuse_env, get_coordinator_trace_attributes

print("🧪 COMBINED TRACE TEST")
print("=" * 50)

# Setup Langfuse with hardcoded credentials
print("🔧 Setting up Langfuse...")
setup_langfuse_env()
print("✅ Langfuse setup complete!")
print()

# Test 1: Direct Langfuse SDK (we know this works)
print("📋 TEST 1: Direct Langfuse SDK")
print("-" * 30)

try:
    langfuse = Langfuse()  # Will use the environment variables we just set
    
    with langfuse.start_as_current_span(name="combined-test-direct") as span:
        print("✅ Direct SDK span created")
        
        langfuse.create_event(
            name="direct-sdk-event",
            level="INFO",
            metadata={"test": "combined_test", "method": "direct_sdk"}
        )
        print("✅ Direct SDK event created")
    
    langfuse.flush()
    print("✅ Direct SDK traces flushed")
    
except Exception as e:
    print(f"❌ Direct SDK failed: {e}")

print()

# Test 2: Strands Agent with tracing
print("📋 TEST 2: Strands Agent with OTEL tracing")
print("-" * 40)

try:
    aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
    if not aws_account_id:
        print("❌ AWS_ACCOUNT_ID not set, skipping Strands Agent test")
    else:
        print(f"✅ AWS Account ID: {aws_account_id}")
        
        # Create Bedrock model
        model = BedrockModel(
            model_id=f"arn:aws:bedrock:us-west-2:{aws_account_id}:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        )
        print("✅ Bedrock model created")
        
        # Create agent with tracing
        agent = Agent(
            model=model,
            system_prompt="You are a test assistant. Respond briefly and cheerfully.",
            trace_attributes=get_coordinator_trace_attributes(SESSION_ID),
        )
        print("✅ Strands Agent created with trace attributes")
        
        # Test interaction
        print("🤖 Testing agent interaction...")
        response = agent("Hello, this is a trace test!")
        print(f"✅ Agent responded: {response[:50]}...")
        
        print("✅ Strands Agent test completed")

except Exception as e:
    print(f"❌ Strands Agent test failed: {e}")

print()

# Test 3: Combined approach - Direct trace + Agent trace in sequence
print("📋 TEST 3: Sequential Direct + Agent tracing")
print("-" * 42)

try:
    # Direct trace first
    langfuse = Langfuse()
    with langfuse.start_as_current_span(name="combined-sequence-test") as span:
        langfuse.create_event(
            name="sequence-start-event",
            level="INFO",
            metadata={"step": "1", "type": "direct_before_agent"}
        )
        print("✅ Step 1: Direct trace created")
    
    # Agent trace second (if AWS setup)
    if aws_account_id:
        response = agent("This is step 2 of the sequence test")
        print("✅ Step 2: Agent trace created")
    
    # Direct trace third
    with langfuse.start_as_current_span(name="combined-sequence-end") as span:
        langfuse.create_event(
            name="sequence-end-event",
            level="INFO",
            metadata={"step": "3", "type": "direct_after_agent"}
        )
        print("✅ Step 3: Final direct trace created")
    
    langfuse.flush()
    print("✅ All traces flushed")

except Exception as e:
    print(f"❌ Sequential test failed: {e}")

print()
print("🎯 SUMMARY")
print("=" * 20)
print("Check your Langfuse dashboard at: https://us.cloud.langfuse.com")
print("Look for traces with:")
print("  - Span names: combined-test-direct, combined-sequence-test")  
print("  - Event names: direct-sdk-event, sequence-start-event")
print("  - Service: concierge-sales-assistant (from OTEL)")
print(f"  - Session ID: {SESSION_ID}")
print()
print("🔍 Both direct SDK and OTEL traces should appear!")
print("   If only direct SDK traces appear, there's an OTEL configuration issue.")
print("   If both appear, your setup is working correctly!")