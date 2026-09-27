import re


SKILLS = [
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "react",
    "node.js",
    "sql",
    "mysql",
    "mongodb",
    "flask",
    "django",
    "git",
    "github",
    "machine learning",
    "data analysis",
    "c",
    "c++"
]


ATS_KEYWORDS = [
    "problem solving",
    "communication",
    "teamwork",
    "leadership",
    "analytical",
    "development",
    "testing",
    "debugging",
    "api",
    "database",
    "responsive",
    "optimization"
]


def analyze_resume(resume_text):

    text = resume_text.lower()

    # -----------------------------
    # FIND SKILLS
    # -----------------------------

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    missing_skills = [
        skill for skill in SKILLS
        if skill not in found_skills
    ]


    # -----------------------------
    # FIND RESUME SECTIONS
    # -----------------------------

    sections = {
        "education": "education",
        "experience": "experience",
        "skills": "skills",
        "projects": "projects"
    }

    found_sections = []

    for section, keyword in sections.items():

        if keyword in text:
            found_sections.append(section)


    # -----------------------------
    # ATS SCORE BREAKDOWN
    # -----------------------------

    score_breakdown = {
        "contact_information": 0,
        "summary_objective": 0,
        "education": 0,
        "experience": 0,
        "projects": 0,
        "technical_skills": 0,
        "resume_content": 0
    }


    # Contact Information - 20 points

    if re.search(r"\b[\w.-]+@[\w.-]+\.\w+\b", text):
        score_breakdown["contact_information"] += 10

    if re.search(r"\b\d{10}\b", text):
        score_breakdown["contact_information"] += 10


    # Summary / Objective - 10 points

    if "summary" in text or "objective" in text:
        score_breakdown["summary_objective"] = 10


    # Education - 10 points

    if "education" in text:
        score_breakdown["education"] = 10


    # Experience - 10 points

    if "experience" in text:
        score_breakdown["experience"] = 10


    # Projects - 10 points

    if "projects" in text:
        score_breakdown["projects"] = 10


    # Technical Skills - 20 points

    score_breakdown["technical_skills"] = min(
        len(found_skills) * 2,
        20
    )


    # Resume Content - 10 points

    if len(resume_text) >= 1000:
        score_breakdown["resume_content"] = 10


    # Final ATS Score

    score = round(
    (sum(score_breakdown.values()) / 90) * 100
)

    score_percentages = {
    "contact_information": score_breakdown["contact_information"] * 5,
    "summary_objective": score_breakdown["summary_objective"] * 10,
    "education": score_breakdown["education"] * 10,
    "experience": score_breakdown["experience"] * 10,
    "projects": score_breakdown["projects"] * 10,
    "technical_skills": score_breakdown["technical_skills"] * 5,
    "resume_content": score_breakdown["resume_content"] * 10
}


    # -----------------------------
    # STRENGTHS
    # -----------------------------

    strengths = []

    if len(found_skills) >= 5:
        strengths.append(
            "Good technical skill coverage"
        )

    if "projects" in text:
        strengths.append(
            "Projects section is included"
        )

    if "education" in text:
        strengths.append(
            "Education details are included"
        )

    if "experience" in text:
        strengths.append(
            "Experience section is included"
        )

    if "summary" in text or "objective" in text:
        strengths.append(
            "Professional summary is included"
        )

    if re.search(
        r"\b[\w.-]+@[\w.-]+\.\w+\b",
        text
    ):
        strengths.append(
            "Email contact information is available"
        )


    # -----------------------------
    # WEAKNESSES
    # -----------------------------

    weaknesses = []

    if len(found_skills) < 5:
        weaknesses.append(
            "Technical skills section can be improved"
        )

    if "projects" not in text:
        weaknesses.append(
            "Projects section is missing"
        )

    if "experience" not in text:
        weaknesses.append(
            "Experience section is missing"
        )

    if "education" not in text:
        weaknesses.append(
            "Education section is missing"
        )

    if "summary" not in text and "objective" not in text:
        weaknesses.append(
            "Professional summary or objective is missing"
        )

    if not re.search(
        r"\b[\w.-]+@[\w.-]+\.\w+\b",
        text
    ):
        weaknesses.append(
            "Email contact information is missing"
        )

    if len(resume_text) < 1000:
        weaknesses.append(
            "Resume content is too short"
        )

    # -----------------------------
    # IMPROVEMENT SUGGESTIONS
    # -----------------------------

    suggestions = []

    if len(found_skills) < 5:
        suggestions.append(
            "Add more relevant technical skills for your target role."
        )

    if "projects" not in text:
        suggestions.append(
            "Add 2-3 practical projects with technologies and measurable results."
        )

    if "experience" not in text:
        suggestions.append(
            "Add an Experience section if you have internship, freelance, or relevant experience."
        )

    if "education" not in text:
        suggestions.append(
            "Add your education details, degree, institution, and graduation year."
        )

    if "summary" not in text and "objective" not in text:
        suggestions.append(
            "Add a concise professional summary tailored to the target role."
        )

    if not re.search(
        r"\b[\w.-]+@[\w.-]+\.\w+\b",
        text
    ):
        suggestions.append(
            "Add a professional email address to your contact information."
        )

    if len(resume_text) < 1000:
        suggestions.append(
            "Add more relevant detail while keeping the resume concise."
        )


    # -----------------------------
    # RETURN ANALYSIS
    # -----------------------------

    return {
        "score": score,
        "score_breakdown": score_breakdown,
        "score_percentages": score_percentages,
        "found_skills": found_skills,
        "missing_skills": missing_skills,
       "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }


def match_job(resume_text, job_description):

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    matching_skills = []
    missing_skills = []

    for skill in SKILLS:

        skill_lower = skill.lower()

        if skill_lower in job_description:

            if skill_lower in resume_text:
                matching_skills.append(skill)

            else:
                missing_skills.append(skill)


    total_job_skills = (
        len(matching_skills)
        + len(missing_skills)
    )


    if total_job_skills > 0:

        match_percentage = round(
            (
                len(matching_skills)
                / total_job_skills
            ) * 100
        )

    else:

        match_percentage = 0


    return {
        "match_percentage": match_percentage,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }