TEST_CASES = [
    {
        "category": "RAG Unique",
        "query": "What are the password requirements for IT security?",
        "ground_truth": "16 characters containing at least one uppercase letter, one number, and one special character. Must be rotated every 90 days. Biometric login is required."
    },
    {
        "category": "RAG Unique",
        "query": "When using public Wi-Fi, what must employees connect to before reading emails?",
        "ground_truth": "The GlobalCorp Cisco AnyConnect VPN."
    },
    {
        "category": "RAG Unique",
        "query": "How should employees report a suspected phishing email?",
        "ground_truth": "Click the 'PhishAlarm' button in Outlook. Forwarding to IT Support is no longer approved."
    },
    {
        "category": "RAG > LC",
        "query": "How many weeks of parental leave do non-birthing parents receive, and is there a phase-back period?",
        "ground_truth": "16 weeks fully paid. There is a 4-week phase-back period working 50 percent capacity at 100 percent pay."
    },
    {
        "category": "RAG > LC",
        "query": "How many days of standard PTO do salaried employees accrue per year if they have 6 years of tenure?",
        "ground_truth": "25 days of PTO annually."
    },
    {
        "category": "RAG > LC",
        "query": "After how many years of employment is an employee eligible for a paid sabbatical?",
        "ground_truth": "After 7 years of continuous full-time employment, an employee gets a 6-week paid sabbatical approved 6 months in advance."
    },
    {
        "category": "LC > RAG",
        "query": "According to the GlobalCorp Travel Policy, what is the exact daily per diem for a business trip to a high-cost city (e.g., Tokyo or London)?",
        "ground_truth": "$120 per day."
    },
    {
        "category": "LC > RAG",
        "query": "Regarding GlobalCorp's parental leave, what is the specific rule if a scheduled company holiday falls during the leave period?",
        "ground_truth": "The leave duration is automatically extended by one business day."
    },
    {
        "category": "LC > RAG",
        "query": "What is the GlobalCorp monthly childcare subsidy amount per child?",
        "ground_truth": "$500 per child monthly."
    },
    {
        "category": "LC Unique",
        "query": "What is the GlobalCorp Travel Reimbursement Hotline phone number?",
        "ground_truth": "1-888-GLOBAL-TRV."
    },
    {
        "category": "LC Unique",
        "query": "What is the GlobalCorp Ethics Hotline 24/7 phone number mentioned in the Code of Conduct?",
        "ground_truth": "1-800-555-0199."
    },
    {
        "category": "LC Unique",
        "query": "What is the maximum nightly hotel rate for NYC as per GlobalCorp policy?",
        "ground_truth": "$400."
    }
]
