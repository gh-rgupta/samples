#!/usr/bin/env python3
"""
Hardcoded trace test - exact copy of the working test.py pattern with hardcoded credentials.
"""

from langfuse import Langfuse

# Hardcoded credentials that we know work
langfuse_host = "https://us.cloud.langfuse.com"
langfuse_public_key = "pk-lf-1d537221-c3d2-4b1f-8a42-2de2601de53d"
langfuse_secret_key = "sk-lf-357ab81a-dc5d-4736-948e-cdcf0a54783a"

print(f"Connecting to Langfuse at: {langfuse_host}")

# Initialize Langfuse client
langfuse = Langfuse(
    public_key=langfuse_public_key,
    secret_key=langfuse_secret_key,
    host=langfuse_host
)

try:
    # Test basic connection first
    print("Testing connection to Langfuse...")
    
    # Create a trace ID first
    trace_id = langfuse.create_trace_id()
    print(f"✅ Created trace ID: {trace_id}")
    
    # Start a span as current context
    with langfuse.start_as_current_span(name="hardcoded-test-span") as span:
        print("✅ Started span in context")
        
        # Update the current span with more information
        langfuse.update_current_span(
            metadata={"completed": True, "source": "hardcoded-test-script", "test_type": "concierge_app_debug"}
        )
        print("✅ Updated span")
        
        # Create an event (without trace_id since we're in context)
        langfuse.create_event(
            name="concierge-debug-event",
            level="INFO",
            metadata={"message": "Hardcoded test completed", "app": "concierge_sales_assistant"}
        )
        print("✅ Created event")
        
        # Create a score for the current trace
        langfuse.create_score(
            name="debug-test-score",
            value=1.0
        )
        print("✅ Created score")
    
    print("✅ Span completed")
    
    # Ensure data is sent
    langfuse.flush()
    print("✅ Data flushed to Langfuse")
    
    # Get trace URL for verification  
    current_trace_id = langfuse.get_current_trace_id()
    if current_trace_id:
        trace_url = langfuse.get_trace_url(current_trace_id)
        print(f"✅ Trace URL: {trace_url}")
    
    print("✅ Hardcoded trace sent successfully!")
    print()
    print("🔍 Check your Langfuse dashboard:")
    print("   URL: https://us.cloud.langfuse.com")
    print("   Look for traces with:")
    print("   - Event name: concierge-debug-event")
    print("   - Span name: hardcoded-test-span")
    print("   - Metadata: source=hardcoded-test-script")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e)}")
    print("\nThis should not happen if test.py worked!")