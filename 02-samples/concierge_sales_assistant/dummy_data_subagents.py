COMPLETE_SALESFORCE_DATA = {
    "orders": [
        # ===== ACTIVE ORDERS =====
        {"doctor": "Dr. Sarah Johnson", "order_id": "ORD-001", "status": "On Hold", 
         "product": "Guardant360", "date": "2024-01-15", "amount": "\$2,500", "quantity": 1},
        
        {"doctor": "Dr. Michael Chen", "order_id": "ORD-002", "status": "Completed", 
         "product": "GuardantOMNI", "date": "2024-01-14", "amount": "\$3,200", "quantity": 1},
        
        {"doctor": "Dr. Emily Rodriguez", "order_id": "ORD-004", "status": "On Hold", 
         "product": "Guardant360", "date": "2024-01-13", "amount": "\$2,500", "quantity": 1},
        
        {"doctor": "Dr. Shafique", "order_id": "ORD-009", "status": "Completed", 
         "product": "Guardant360", "date": "2024-01-20", "amount": "\$2,500", "quantity": 1},
        
        {"doctor": "Dr. Shafique", "order_id": "ORD-010", "status": "Processing", 
         "product": "GuardantOMNI", "date": "2024-01-22", "amount": "\$6,400", "quantity": 2},
        
        {"doctor": "Dr. Julie", "order_id": "ORD-012", "status": "On Hold", 
         "product": "Guardant360", "date": "2024-01-21", "amount": "\$2,500", "quantity": 1},
        
        {"doctor": "Dr. Julie", "order_id": "ORD-013", "status": "Completed", 
         "product": "Guardant Reveal", "date": "2024-01-18", "amount": "\$3,600", "quantity": 2},
        
        {"doctor": "Dr. Smith", "order_id": "ORD-020", "status": "Processing", 
         "product": "Guardant360", "date": "2024-01-19", "amount": "\$2,500", "quantity": 1},
        
        # ===== CANCELLED ORDERS (Q4 2023) =====
        {"doctor": "Dr. Emily Rodriguez", "order_id": "ORD-014", "status": "Cancelled", 
         "product": "Guardant360", "date": "2023-12-15", "amount": "\$2,500", "quantity": 1},
        
        {"doctor": "Dr. Emily Rodriguez", "order_id": "ORD-015", "status": "Cancelled", 
         "product": "GuardantOMNI", "date": "2023-12-20", "amount": "\$3,200", "quantity": 1},
        
        {"doctor": "Dr. Emily Rodriguez", "order_id": "ORD-016", "status": "Cancelled", 
         "product": "Guardant Reveal", "date": "2024-01-05", "amount": "\$1,800", "quantity": 1},
        
        {"doctor": "Dr. James Wilson", "order_id": "ORD-017", "status": "Cancelled", 
         "product": "Guardant360", "date": "2023-11-28", "amount": "\$5,000", "quantity": 2},
        
        {"doctor": "Dr. James Wilson", "order_id": "ORD-018", "status": "Cancelled", 
         "product": "GuardantOMNI", "date": "2023-12-10", "amount": "\$3,200", "quantity": 1},
        
        {"doctor": "Dr. Michael Chen", "order_id": "ORD-019", "status": "Cancelled", 
         "product": "Guardant360", "date": "2023-10-25", "amount": "\$2,500", "quantity": 1},
    ],
    
    # ===== STARK COMPLIANCE DATA =====
    "stark_compliance": [
        {"doctor": "Dr. Shafique", "annual_limit": 5000, "current_spent": 3250, 
         "remaining": 1750, "risk_level": "Medium", "percentage_used": 65.0},
        
        {"doctor": "Dr. Julie", "annual_limit": 3500, "current_spent": 2100, 
         "remaining": 1400, "risk_level": "Low", "percentage_used": 60.0},
        
        {"doctor": "Dr. Sarah Johnson", "annual_limit": 6000, "current_spent": 4200, 
         "remaining": 1800, "risk_level": "High", "percentage_used": 70.0},
        
        {"doctor": "Dr. Michael Chen", "annual_limit": 4000, "current_spent": 2800, 
         "remaining": 1200, "risk_level": "Medium", "percentage_used": 70.0},
        
        {"doctor": "Dr. Emily Rodriguez", "annual_limit": 7000, "current_spent": 5600, 
         "remaining": 1400, "risk_level": "High", "percentage_used": 80.0},
        
        {"doctor": "Dr. Smith", "annual_limit": 4500, "current_spent": 2800, 
         "remaining": 1700, "risk_level": "Medium", "percentage_used": 62.2},
    ]
}

COMPLETE_VEEVA_DATA = {
    "engagements": [
        {
            "doctor": "Dr. Julie", 
            "engagement_id": "ENG-012", 
            "type": "Email Communication", 
            "date": "2024-01-22", 
            "rep": "Maria Garcia", 
            "outcome": "Positive - Questions answered", 
            "talking_points": [
                "Technical specifications clarified", 
                "Ordering process simplified", 
                "Support availability confirmed"
            ]
        },
        
        {
            "doctor": "Dr. Shafique", 
            "engagement_id": "ENG-013", 
            "type": "In-Person Visit", 
            "date": "2024-01-20", 
            "rep": "John Smith", 
            "outcome": "Positive - Discussed volume pricing", 
            "talking_points": [
                "Volume discounts available", 
                "Bulk ordering process", 
                "Implementation support"
            ]
        },
        
        {
            "doctor": "Dr. Sarah Johnson", 
            "engagement_id": "ENG-001", 
            "type": "In-Person Visit", 
            "date": "2024-01-15", 
            "rep": "John Smith", 
            "outcome": "Positive - Interested in Guardant360", 
            "talking_points": [
                "Guardant360 features", 
                "Turnaround time benefits", 
                "Clinical utility"
            ]
        },
        
        {
            "doctor": "Dr. Smith", 
            "engagement_id": "ENG-014", 
            "type": "Virtual Meeting", 
            "date": "2024-01-18", 
            "rep": "Sarah Chen", 
            "outcome": "Positive - Interested in new products", 
            "talking_points": [
                "Product portfolio overview", 
                "Clinical applications", 
                "Implementation timeline"
            ]
        },
    ]
}

COMPLETE_TABLEAU_DATA = {
    "test_ordering_trends": [
        {
            "product": "Guardant360", 
            "month": "2024-01", 
            "orders": 47, 
            "completed": 44, 
            "cancelled": 3, 
            "growth": "+4.4%", 
            "completion_rate": 93.6
        },
        
        {
            "product": "GuardantOMNI", 
            "month": "2024-01", 
            "orders": 33, 
            "completed": 30, 
            "cancelled": 3, 
            "growth": "+5.4%", 
            "completion_rate": 90.9
        },
        
        {
            "product": "Guardant Reveal", 
            "month": "2024-01", 
            "orders": 31, 
            "completed": 29, 
            "cancelled": 2, 
            "growth": "+20.6%", 
            "completion_rate": 93.5
        },
    ]
}

## for training data, we will connect to actual knowledge based on aws in future
## so no dummy data is provided here
