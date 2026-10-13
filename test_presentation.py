
from presentation_tool import create_presentation

title = "Introduction to Artificial Intelligence"

slides = [
    {
        "title": "Introduction",
        "points": [
            "AI enables machines to perform intelligent tasks.",
            "It uses data and algorithms to solve problems.",
            "AI is used across many industries."
        ]
    },
    {
        "title": "Applications of AI",
        "points": [
            "Healthcare and medical diagnosis",
            "Education and personalized learning",
            "Banking and fraud detection",
            "Chatbots and virtual assistants"
        ]
    },
    {
        "title": "Advantages and Challenges",
        "points": [
            "Automates repetitive tasks",
            "Can analyze large amounts of data",
            "Requires reliable data and careful evaluation",
            "May produce inaccurate results"
        ]
    },
    {
        "title": "Conclusion",
        "points": [
            "AI is transforming many industries.",
            "Responsible development is important.",
            "Human oversight remains valuable."
        ]
    }
]

file_path = create_presentation(title, slides)
print("PowerPoint created successfully!")
print("File location:", file_path)
