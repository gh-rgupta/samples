#!/usr/bin/env python3
"""
Setup script for Langfuse integration.
This script helps you configure and test your Langfuse connection.
"""

import os
import base64
from langfuse import Langfuse

def setup_langfuse_credentials():
    """Interactive setup for Langfuse credentials."""
    
    print("🔧 Langfuse Setup & Configuration")
    print("=" * 50)
    print()
    
    print("📋 Step 1: Get your Langfuse credentials")
    print("   1. Go to https://cloud.langfuse.com")
    print("   2. Sign up or log in")
    print("   3. Create a new project (or select existing)")
    print("   4. Go to Settings → API Keys")
    print("   5. Copy your Public Key and Secret Key")
    print()
    
    # Get credentials from user
    public_key = input("Enter your Langfuse Public Key (pk_lf_...): ").strip()
    secret_key = input("Enter your Langfuse Secret Key (sk_lf_...): ").strip()
    
    if not public_key or not secret_key:
        print("❌ Both keys are required. Please run the script again.")
        return False
    
    if not public_key.startswith("pk_lf_") or not secret_key.startswith("sk_lf_"):
        print("⚠️  Warning: Keys don't have expected prefixes. Continuing anyway...")
    
    print()
    print("🧪 Testing Langfuse connection...")
    
    try:
        # Test the connection
        langfuse = Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host="https://us.cloud.langfuse.com"
        )
        
        # Try to create a simple trace to test
        trace = langfuse.trace(
            name="test_connection",
            metadata={"test": True}
        )
        
        # Flush to ensure it's sent
        langfuse.flush()
        
        print("✅ Connection successful!")
        print()
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("   Please check your credentials and try again.")
        return False
    
    # Set environment variables for current session
    os.environ["LANGFUSE_PUBLIC_KEY"] = public_key
    os.environ["LANGFUSE_SECRET_KEY"] = secret_key
    os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com"
    
    # Set up OTEL configuration
    host = "https://us.cloud.langfuse.com"
    otel_endpoint = f"{host}/api/public/otel/v1/traces"
    auth_token = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
    
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = otel_endpoint
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_token}"
    
    print("📝 Environment variables set for current session:")
    print(f"   LANGFUSE_PUBLIC_KEY={public_key[:10]}...")
    print(f"   LANGFUSE_SECRET_KEY={secret_key[:10]}...")
    print(f"   LANGFUSE_HOST={host}")
    print(f"   OTEL_EXPORTER_OTLP_ENDPOINT={otel_endpoint}")
    print()
    
    print("💡 To make these permanent, add to your shell profile:")
    print(f'   export LANGFUSE_PUBLIC_KEY="{public_key}"')
    print(f'   export LANGFUSE_SECRET_KEY="{secret_key}"')
    print(f'   export LANGFUSE_HOST="{host}"')
    print()
    
    return True

def test_concierge_integration():
    """Test the integration with a simple query."""
    
    print("🚀 Testing Concierge Sales Assistant integration...")
    print("-" * 50)
    
    try:
        # Import here so environment variables are set
        from concierge_sales_assistant import concierge_sales_agent
        
        print("✅ Successfully imported concierge agent")
        
        # Test with a simple query
        test_query = "Show me open cases in my territory"
        print(f"📝 Testing query: \"{test_query}\"")
        
        response = concierge_sales_agent(test_query)
        print(f"✅ Query processed successfully!")
        print(f"📄 Response preview: {str(response)[:150]}...")
        
        print()
        print("🔍 Check your Langfuse dashboard:")
        print("   1. Go to https://cloud.langfuse.com")
        print("   2. Select your project")
        print("   3. Look for traces with tags: 'Concierge-Sales-Assistant'")
        print("   4. You should see both coordinator and sub-agent traces")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing integration: {str(e)}")
        print("   This might be due to missing dependencies or configuration issues.")
        return False

def main():
    """Main setup flow."""
    
    # Check if already configured
    if os.environ.get("LANGFUSE_PUBLIC_KEY") and os.environ.get("LANGFUSE_SECRET_KEY"):
        print("✅ Langfuse credentials already configured!")
        print("🧪 Testing existing configuration...")
        
        if test_concierge_integration():
            print("🎉 Everything is working!")
            return
    
    # Setup credentials
    if setup_langfuse_credentials():
        print("🧪 Testing integration with Concierge Sales Assistant...")
        print()
        
        if test_concierge_integration():
            print()
            print("🎉 Setup complete! Your Concierge Sales Assistant is now")
            print("   connected to Langfuse for observability.")
        else:
            print()
            print("⚠️  Setup completed but integration test failed.")
            print("   Check the error messages above for troubleshooting.")

if __name__ == "__main__":
    main()