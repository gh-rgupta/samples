from strands import Agent, tool
from strands.models import BedrockModel
from constants import SESSION_ID
from dummy_data_subagents import COMPLETE_TABLEAU_DATA
import json

model = BedrockModel(
    model_id="arn:aws:bedrock:us-west-2:558178433193:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)

def query_tableau_data(query: str):
    """Query the dummy Tableau analytics data based on the user query."""
    query_lower = query.lower()
    trends = COMPLETE_TABLEAU_DATA['test_ordering_trends']
    results = []
    
    # Quota and performance queries
    if any(word in query_lower for word in ['quota', 'tracking', 'performance', 'monthly']):
        # Mock quota data with current trends
        total_orders = sum(trend['orders'] for trend in trends)
        total_completed = sum(trend['completed'] for trend in trends)
        monthly_quota = 150  # Mock quota
        
        results = {
            'quota_tracking': {
                'monthly_quota': monthly_quota,
                'current_orders': total_orders,
                'completed_orders': total_completed,
                'quota_achievement': round((total_completed / monthly_quota) * 100, 1),
                'remaining_to_quota': monthly_quota - total_completed,
                'trending': 'Above Target' if total_completed > (monthly_quota * 0.7) else 'Below Target'
            },
            'product_breakdown': trends
        }
    
    # Top performers queries
    elif any(word in query_lower for word in ['top', 'performers', 'territory', 'revenue']):
        # Mock territory performance data
        results = {
            'top_performers': [
                {'rep': 'John Smith', 'territory': 'North Bay', 'revenue': '$45,200', 'orders': 28, 'growth': '+12.5%'},
                {'rep': 'Maria Garcia', 'territory': 'South Valley', 'revenue': '$38,900', 'orders': 24, 'growth': '+8.2%'},
                {'rep': 'Sarah Chen', 'territory': 'East Coast', 'revenue': '$42,100', 'orders': 26, 'growth': '+15.1%'},
                {'rep': 'David Wilson', 'territory': 'Central', 'revenue': '$35,800', 'orders': 22, 'growth': '+6.3%'},
                {'rep': 'Lisa Rodriguez', 'territory': 'West Region', 'revenue': '$41,500', 'orders': 25, 'growth': '+9.8%'}
            ]
        }
    
    # Order volume and trends
    elif any(word in query_lower for word in ['volume', 'trend', 'declining', 'accounts']):
        results = {
            'order_trends': trends,
            'declining_accounts': [
                {'account': 'Pacific Medical Group', 'current_month': 8, 'last_month': 14, 'decline': '-42.9%'},
                {'account': 'Bay Area Oncology', 'current_month': 12, 'last_month': 18, 'decline': '-33.3%'},
                {'account': 'Valley Health System', 'current_month': 15, 'last_month': 21, 'decline': '-28.6%'}
            ]
        }
    
    # Engagement correlation queries
    elif any(word in query_lower for word in ['engagement', 'correlation', 'conversion']):
        results = {
            'engagement_metrics': [
                {'engagement_type': 'In-Person Visit', 'avg_orders_following': 3.2, 'conversion_rate': '85%'},
                {'engagement_type': 'Virtual Meeting', 'avg_orders_following': 2.1, 'conversion_rate': '68%'},
                {'engagement_type': 'Email Communication', 'avg_orders_following': 1.4, 'conversion_rate': '45%'},
                {'engagement_type': 'Phone Call', 'avg_orders_following': 1.8, 'conversion_rate': '52%'}
            ],
            'monthly_conversions': {
                'total_engagements': 156,
                'successful_conversions': 103,
                'conversion_rate': '66.0%'
            }
        }
    
    else:
        # Default overview
        results = {
            'overview': trends,
            'summary': {
                'total_orders': sum(trend['orders'] for trend in trends),
                'total_completed': sum(trend['completed'] for trend in trends),
                'avg_completion_rate': round(sum(trend['completion_rate'] for trend in trends) / len(trends), 1)
            }
        }
    
    return results

tableau_agent = Agent(
    model=model,
    system_prompt="""You are a Tableau analytics specialist assistant with access to real sales performance data, quotas, territory metrics, and engagement analytics.
    Analyze the provided data and give specific, actionable insights. Format your responses clearly with relevant metrics, percentages, and trends.
    When presenting analytics, highlight key performance indicators, trends, and actionable recommendations for sales improvement.""",
    trace_attributes={"session.id": SESSION_ID},
)

@tool
def tableau_assistant(query: str) -> str:
    """Handle Tableau-related queries about analytics, quotas, performance metrics, and territory data."""
    print(f"📊 TABLEAU AGENT: Processing analytics query - '{query}'")
    
    # Query the data
    data_results = query_tableau_data(query)
    
    # Prepare context for the agent
    context = f"User Query: {query}\n\nRelevant Tableau Analytics Data:\n{json.dumps(data_results, indent=2)}"
    
    response = tableau_agent(f"Based on this Tableau analytics data, provide a specific answer with insights and recommendations to the user's query:\n\n{context}")
    return str(response)