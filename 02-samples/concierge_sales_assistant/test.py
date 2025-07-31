import os
from langfuse import Langfuse

# Set default values for testing if environment variables aren't set
langfuse_host = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY", "sk-lf-test")

print(f"Connecting to Langfuse at: {langfuse_host}")

# Initialize Langfuse client
langfuse = Langfuse(
    public_key=langfuse_public_key,
    secret_key=langfuse_secret_key,
    host=langfuse_host
)

# Debug: Check available methods
print("Available methods on Langfuse client:")
available_methods = [method for method in dir(langfuse) if not method.startswith('_')]
print(available_methods)

try:
    # Test using the correct Langfuse SDK API patterns
    print("\nTesting Langfuse trace creation...")
    
    # Create a trace ID first
    trace_id = langfuse.create_trace_id()
    print(f"✅ Created trace ID: {trace_id}")
    
    # Start a span as current context
    with langfuse.start_as_current_span(name="test-span") as span:
        print("✅ Started span in context")
        
        # Update the current span with more information
        langfuse.update_current_span(
            metadata={"completed": True, "source": "test-script"}
        )
        print("✅ Updated span")
        
        # Create an event (without trace_id since we're in context)
        langfuse.create_event(
            name="test-event",
            level="INFO",
            metadata={"message": "Connection test completed"}
        )
        print("✅ Created event")
        
        # Create a score for the current trace
        langfuse.create_score(
            name="test-score",
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
    
    print("✅ Trace sent successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e)}")
    print("\nTroubleshooting:")
    print("1. Make sure Langfuse is running at", langfuse_host)
    print("2. Check if you need to create a project and get API keys from the UI")
    print("3. Verify the Langfuse SDK version: pip show langfuse")
    print("4. Try accessing the Langfuse UI to set up a project first")
