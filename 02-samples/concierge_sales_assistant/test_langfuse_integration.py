#!/usr/bin/env python3
"""
Test script to verify Langfuse integration with the Concierge Sales Assistant.
Run this to test observability without running the full interactive application.
"""

import os
from concierge_sales_assistant import concierge_sales_agent

def test_langfuse_integration():
    """Test the Langfuse integration with sample queries."""
    
    print("🧪 Testing Langfuse Integration with Concierge Sales Assistant")
    print("=" * 70)
    
    # Check if Langfuse environment variables are set
    langfuse_public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    
    if not langfuse_public_key or not langfuse_secret_key:
        print("⚠️  WARNING: Langfuse credentials not found in environment variables.")
        print("   Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY to enable tracing.")
        print("   Continuing test without actual trace upload...")
        print()
    else:
        print("✅ Langfuse credentials found in environment variables")
        print("✅ Traces will be sent to Langfuse dashboard")
        print()
    
    # Test queries for different agents
    test_queries = [
        {
            "query": "Show me open cases in my territory",
            "expected_agent": "Salesforce Agent",
            "description": "Single-domain Salesforce query"
        },
        # {
        #     "query": "How am I tracking against my monthly quota?",
        #     "expected_agent": "Tableau Agent", 
        #     "description": "Single-domain Tableau query"
        # },
        # {
        #     "query": "What are the sample requirements for Guardant360?",
        #     "expected_agent": "Training Agent",
        #     "description": "Single-domain Training query"
        # },
        # {
        #     "query": "What should I know before my call with Dr. Smith?",
        #     "expected_agent": "Multiple Agents",
        #     "description": "Multi-domain composite query"
        # }
    ]
    
    print("🚀 Running test queries...")
    print()
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"Query: \"{test_case['query']}\"")
        print(f"Expected routing: {test_case['expected_agent']}")
        print("-" * 50)
        
        try:
            # Run the query through the concierge agent
            response = concierge_sales_agent(test_case['query'])
            print(f"✅ Query processed successfully")
            print(f"Response preview: {str(response)[:100]}...")
            
        except Exception as e:
            print(f"❌ Error processing query: {str(e)}")
            
        print()
        print("=" * 70)
        print()
    
    print("🎉 Test completed!")
    print()
    print("📊 Next Steps:")
    print("1. Check your Langfuse dashboard for traces")
    print("2. Look for traces tagged with 'Concierge-Sales-Assistant'")
    print("3. Verify multi-agent routing is captured correctly")
    print("4. Check trace attributes for session and agent information")
    print()
    print("🔗 Langfuse Dashboard: https://cloud.langfuse.com")

if __name__ == "__main__":
    test_langfuse_integration()