from typing import Dict, List, Optional


_SECTION_ORDER = {
    "summary": 0,
    "experience": 1,
    "projects": 2,
    "skills": 3,
}


def _suggestion(
    priority: str,
    category: str,
    title: str,
    what_to_change: str,
    where_to_place: str,
    current_text: str,
    example: str,
    ats_reason: str,
) -> Dict[str, str]:
    return {
        "priority": priority,
        "category": category,
        "title": title,
        "what_to_change": what_to_change,
        "where_to_place": where_to_place,
        "current_text": current_text,
        "example": example,
        "ats_reason": ats_reason,
    }


def generate_enhancement_suggestions(
    resume_text: str,
    parsed_resume: Dict,
    scores: Dict,
    skill_validation: Dict,
    jd_keywords: Optional[List[str]] = None,
) -> List[Dict[str, str]]:
    """Create concrete, placement-aware resume improvements from existing analysis data."""
    suggestions: List[Dict[str, str]] = []
    summary = (parsed_resume.get("professional_summary") or "").strip()
    experience = [item for item in parsed_resume.get("experience", []) if isinstance(item, dict)]
    projects = [item for item in parsed_resume.get("projects", []) if isinstance(item, dict)]
    skills = [str(skill) for skill in parsed_resume.get("skills", []) if skill]
    action_verbs = parsed_resume.get("action_verbs", [])
    keywords = [str(keyword) for keyword in parsed_resume.get("keywords", []) if keyword]

    if not summary:
        suggestions.append(_suggestion(
            "high", "Professional Summary", "Add a targeted professional summary",
            "Add two or three lines that identify your role, strongest tools, and measurable value.",
            "Place directly below your name and contact information.",
            "No professional summary was detected.",
            "Full-Stack Developer skilled in React, Node.js, and Python, building scalable web applications and REST APIs. Improved application performance by 35% through caching and query optimization.",
            "A concise summary gives ATS systems a high-value keyword block and helps recruiters understand your target role immediately.",
        ))

    descriptions = " ".join(str(item.get("description", "")) for item in experience)
    has_metrics = any(char.isdigit() for char in descriptions)
    if experience and (scores.get("content_score", 25) < 20 or not has_metrics):
        title = "Rewrite experience bullets with impact"
        current = descriptions[:180] if descriptions else "Experience bullets contain limited achievement detail."
        job_title = experience[0].get("job_title") or "your role"
        suggestions.append(_suggestion(
            "high", "Experience", title,
            "Start each bullet with an action verb, name the technology, explain the work, and finish with a measurable result.",
            f"Replace the weakest bullets under Experience > {job_title}.",
            current,
            "Developed a FastAPI service with PostgreSQL that reduced average API response time by 40% and supported 10K monthly requests.",
            "Action verbs, exact technologies, and measurable outcomes improve keyword matching and demonstrate credible impact.",
        ))

    unvalidated = [str(skill) for skill in skill_validation.get("unvalidated_skills", []) if skill]
    if unvalidated:
        skill = unvalidated[0]
        suggestions.append(_suggestion(
            "high", "Skills Evidence", f"Prove your {skill} skill with evidence",
            f"Mention {skill} in a project or experience bullet and describe how you used it.",
            "Place it in the relevant Project or Experience bullet, not only in the Skills list.",
            f"{skill} appears in Skills but was not found in project or experience evidence.",
            f"Built a production feature using {skill}, improving reliability by 25% and reducing manual testing time by 6 hours per release.",
            "ATS systems and recruiters trust a skill more when the same term appears in achievement context.",
        ))

    missing = []
    for keyword in jd_keywords or []:
        if keyword.lower() not in resume_text.lower() and keyword.lower() not in missing:
            missing.append(keyword)
    if missing:
        keyword_text = ", ".join(missing[:3])
        suggestions.append(_suggestion(
            "high", "Job Match", "Add missing job-description keywords naturally",
            f"Use these relevant terms where truthful: {keyword_text}.",
            "Add them to the Skills section and one supporting Experience or Projects bullet.",
            f"Missing or unmatched JD terms: {keyword_text}.",
            f"Skills: {keyword_text}\nExperience bullet: Implemented {missing[0]} to deliver a measurable improvement for the product.",
            "Natural keyword placement improves targeted matching without keyword stuffing.",
        ))

    if not projects:
        suggestions.append(_suggestion(
            "medium", "Projects", "Add two evidence-based projects",
            "Add projects that show the tools in your Skills section being used to solve a real problem.",
            "Add a Projects section after Experience or Education.",
            "No structured projects were detected.",
            "Resume ATS Analyzer | Python, FastAPI, NLP\nBuilt a resume scoring API that analyzed PDF resumes and returned actionable ATS recommendations.",
            "Projects give ATS systems additional technical keywords and prove that listed skills were applied.",
        ))

    if len(action_verbs) < 5:
        suggestions.append(_suggestion(
            "medium", "Writing", "Replace weak bullet openings",
            "Begin bullets with verbs such as Developed, Automated, Optimized, Implemented, or Led.",
            "Update the first word of bullets in Experience and Projects.",
            f"Only {len(action_verbs)} strong action verbs were detected.",
            "Optimized database queries to reduce report generation time by 30%.",
            "Strong verbs improve scanning clarity and make accomplishments easier for ATS and recruiters to identify.",
        ))

    suggestions.sort(key=lambda item: (_SECTION_ORDER.get(item["category"].lower(), 9), item["priority"]))
    return suggestions[:6]
