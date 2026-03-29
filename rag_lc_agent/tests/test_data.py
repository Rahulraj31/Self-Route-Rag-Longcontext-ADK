TEST_CASES = [
    {
        "category": "RAG_ONLY",
        "query": "what to do if an employee suspects an email is a phishing attempt",
        "ground_truth": "If an employee suspects an email is a phishing attempt, they must click the 'PhishAlarm' button in Outlook. Forwarding the email to IT Support is no longer the approved method",
        "expected_route": "rag"
    },
    {
        "category": "LONG_CONTEXT_ONLY",
        "query": "What are the allowed hotel rates for New York City, San Francisco, and DC?",
        "ground_truth": "The maximum nightly rate for these cities is $400.",
        "expected_route": "long_context"
    },
    {
        "category": "AMBIGUOUS",
        "query": "What are the requirements for business travel?",
        "ground_truth": "Requires Department Head approval 3 weeks prior, CFO approval for international, and specific class restrictions based on flight duration.",
        "expected_route": "long_context"
    },
    {
        "category": "FAIL_RETRIEVAL",
        "query": "Tell me about the monthly childcare subsidy amount for employees with children under 5.",
        "ground_truth": "GlobalCorp provides a monthly childcare subsidy of $500 per child for children under the age of 5.",
        "expected_route": "long_context"
    },
    {
        "category": "EDGE_CASE_SHORT",
        "query": "Hotel NYC?",
        "ground_truth": "$400 per night max.",
        "expected_route": "long_context"
    },
    {
        "category": "EDGE_CASE_MULTI_HOP",
        "query": "If I am a remote employee with a child under 5, what financial support am I eligible for?",
        "ground_truth": "$500 monthly childcare subsidy, $100 monthly remote work stipend, and $1000 one-time WFH stipend.",
        "expected_route": "long_context"
    }
]
