#!/usr/bin/env python3
"""
Script to verify traces are being sent to Langfuse with hardcoded credentials.
"""

import os
import time
import requests
from langfuse import Langfuse
from langfuse_config import setup_langfuse_env

# Setup environment with hardcoded credentials
print("🔧 Setting up Langfuse with hardcoded credentials...")
setup_langfuse_env()
print()

# Double-check the credentials are set
print("🔍 Credential verification:")
print(f"   LANGFUSE_HOST: {os.environ.get('LANGFUSE_HOST', 'Not set')}")
print(f"   LANGFUSE_PUBLIC_KEY: {os.environ.get('LANGFUSE_PUBLIC_KEY', 'Not set')[:20]}...")
print(f"   LANGFUSE_SECRET_KEY: {os.environ.get('LANGFUSE_SECRET_KEY', 'Not set')[:20]}...")
print()

# Test direct Langfuse connection
print("🧪 Testing direct Langfuse connection...")
try:
    langfuse = Langfuse()
    
    # Create a test trace directly
    with langfuse.start_as_current_span(name="verification-test") as span:
        print("✅ Direct trace created!")
        langfuse.create_event(
            name="verification-event",
            level="INFO",
            metadata={"test": "direct_connection", "timestamp": time.time()}
        )
        print("✅ Event logged!")
    
    # Flush to ensure it's sent
    langfuse.flush()
    print("✅ Traces flushed!")
    
except Exception as e:
    print(f"❌ Direct Langfuse connection failed: {e}")

print()

# Test OTEL endpoint
print("🌐 Testing OTEL endpoint connectivity...")
try:
    otel_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
    otel_headers = os.environ.get("OTEL_EXPORTER_OTLP_TRACES_HEADERS")
    
    if not otel_endpoint:
        print("❌ OTEL endpoint not configured")
    else:
        print(f"   Endpoint: {otel_endpoint}")
        print(f"   Headers configured: {'Yes' if otel_headers else 'No'}")
        
        # Test basic connectivity (this will likely fail but shows if endpoint is reachable)
        try:
            response = requests.get(otel_endpoint.replace("/v1/traces", "/health"), timeout=5)
            print(f"   Health check response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   Health check failed (expected): {e}")
            print("   This is normal - OTEL endpoints don't usually have health checks")

except Exception as e:
    print(f"❌ OTEL connectivity test failed: {e}")

print()
print("🔍 Environment Summary:")
print(f"   LANGFUSE_HOST: {os.environ.get('LANGFUSE_HOST', 'Not set')}")
print(f"   OTEL_SERVICE_NAME: {os.environ.get('OTEL_SERVICE_NAME', 'Not set')}")
print(f"   OTEL_TRACES_EXPORTER: {os.environ.get('OTEL_TRACES_EXPORTER', 'Not set')}")

print()
print("📋 Next Steps:")
print("1. Check Langfuse dashboard: https://us.cloud.langfuse.com")
print("2. Look for traces from service: concierge-sales-assistant")
print("3. Check if project exists and API keys are correct")
print("4. Verify traces appear within 1-2 minutes of running this script")