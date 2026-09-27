from utils.ai_analyzer import generate_ai_analysis

resume_text = """
Tarun Kumar
Computer Science Engineering Student

Skills:
Python, Java, JavaScript, HTML, CSS, Flask, SQL

Projects:
AI Resume Analyzer
Library Management System

Education:
Bachelor of Technology in Computer Science Engineering
"""

result = generate_ai_analysis(resume_text)

print("\n===== AI RESUME ANALYSIS =====\n")
print(result)