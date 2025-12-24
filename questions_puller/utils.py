PHASE_WEIGHTS = {
    "primary": {
        "Curiosity Activation": 5,
        "Engagement Sustainment": 5,
        "Personal Relevance Formation": 4,
        "Passion-Driven Mastery": 1
    },
    "secondary": {
        "Curiosity Activation": 4,
        "Engagement Sustainment": 4,
        "Personal Relevance Formation": 5,
        "Passion-Driven Mastery": 2
    },
    "highered": {
        "Curiosity Activation": 1,
        "Engagement Sustainment": 2,
        "Personal Relevance Formation": 6,
        "Passion-Driven Mastery": 6
    },
    "lifelong": {
        "Curiosity Activation": 1,
        "Engagement Sustainment": 2,
        "Personal Relevance Formation": 7,
        "Passion-Driven Mastery": 5
    }
}

PHASE_SEQUENCES = {
    "primary": [
        "Curiosity Activation",
        "Curiosity Activation",
        "Curiosity Activation",
        "Engagement Sustainment",
        "Curiosity Activation",
        "Engagement Sustainment",
        "Engagement Sustainment",
        "Curiosity Activation",
        "Personal Relevance Formation",
        "Engagement Sustainment",
        "Personal Relevance Formation",
        "Engagement Sustainment",
        "Personal Relevance Formation",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
    ],

    "secondary": [
        "Curiosity Activation",
        "Curiosity Activation",
        "Engagement Sustainment",
        "Curiosity Activation",
        "Engagement Sustainment",
        "Curiosity Activation",
        "Engagement Sustainment",
        "Personal Relevance Formation",
        "Engagement Sustainment",
        "Personal Relevance Formation",
        "Personal Relevance Formation",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
    ],

    "highered": [
        "Curiosity Activation",
        "Engagement Sustainment",
        "Engagement Sustainment",
        "Personal Relevance Formation",
        "Personal Relevance Formation",
        "Personal Relevance Formation",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
        "Passion-Driven Mastery",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
        "Passion-Driven Mastery",
        "Passion-Driven Mastery",
    ],

    "lifelong": [
        "Curiosity Activation",
        "Engagement Sustainment",
        "Personal Relevance Formation",
        "Engagement Sustainment",
        "Personal Relevance Formation",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
        "Personal Relevance Formation",
        "Passion-Driven Mastery",
    ]
}

DOMAIN_MAP = {
    "STEM": "STEM",
    "Arts & Creative Expression": "Arts",
    "Business, Economics & Entrepreneurship": "Business",
    "Health, Medicine & Life Sciences": "Health"
}

DOMAINS = ["STEM", "Arts", "Business", "Health"]

PHASE_ORDER = [
    "Curiosity Activation",
    "Engagement Sustainment",
    "Personal Relevance Formation",
    "Passion-Driven Mastery"
]