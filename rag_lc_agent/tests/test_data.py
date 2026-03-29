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
        "query": "Exactly how much is the one-time remote work stipend provided to new employees?",
        "ground_truth": "$1,000 one-time WFH stipend to purchase an ergonomic chair, desk, and external monitor."
    },
    {
        "category": "LC > RAG",
        "query": "What are the minimum internet download and upload speed requirements for remote employees to receive the stipend?",
        "ground_truth": "Minimum download speed of 100 Mbps and upload speed of 20 Mbps."
    },
    {
        "category": "LC > RAG",
        "query": "Which specific laptop models are company-issued for remote work, and is USB mass storage allowed?",
        "ground_truth": "MacBook Pro M3 or Dell XPS 15. USB mass storage devices are strictly disabled and prohibited."
    }
]
