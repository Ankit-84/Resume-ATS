from typing import Dict, List


def build_section_completeness(parsed_resume: Dict) -> Dict:
    checks = [
        ("contact", "Contact information", bool(parsed_resume.get("email") or parsed_resume.get("phone")), "Add email and phone beside your name."),
        ("summary", "Professional summary", bool((parsed_resume.get("professional_summary") or "").strip()), "Add a 2-3 line summary below your contact details."),
        ("skills", "Skills", len(parsed_resume.get("skills", [])) >= 3, "Add a focused Technical Skills section with role-relevant tools."),
        ("experience", "Experience", bool(parsed_resume.get("experience")), "Add work, internship, freelance, or volunteer experience."),
        ("projects", "Projects", bool(parsed_resume.get("projects")), "Add 2-3 projects with technologies and measurable outcomes."),
        ("education", "Education", bool(parsed_resume.get("education")), "Add degree, institution, and graduation year."),
        ("certifications", "Certifications", bool(parsed_resume.get("certifications")), "Add relevant certifications or remove this section if not applicable."),
        ("links", "Professional links", bool(parsed_resume.get("linkedin") or parsed_resume.get("github")), "Add LinkedIn, GitHub, or portfolio links in the contact header."),
    ]
    sections = [
        {"key": key, "label": label, "complete": complete, "tip": tip}
        for key, label, complete, tip in checks
    ]
    completed = sum(item["complete"] for item in sections)
    return {"sections": sections, "completed": completed, "total": len(sections), "percentage": round(completed / len(sections) * 100)}


def build_rewrite_mode(parsed_resume: Dict, enhancement_suggestions: List[Dict]) -> Dict:
    summary = (parsed_resume.get("professional_summary") or "").strip()
    skills = [str(skill) for skill in parsed_resume.get("skills", []) if skill]
    experience = [item for item in parsed_resume.get("experience", []) if isinstance(item, dict)]
    projects = [item for item in parsed_resume.get("projects", []) if isinstance(item, dict)]
    cards = []
    cards.append({
        "section": "Professional Summary",
        "before": summary or "No professional summary detected.",
        "after": (
            f"Results-focused professional skilled in {', '.join(skills[:5]) or 'modern tools and technologies'}. "
            "Built practical solutions, improved delivery quality, and bring a measurable, user-focused approach to every project."
        ),
        "why": "Places your target keywords and value proposition near the top of the resume.",
    })
    if experience:
        first = experience[0]
        before = first.get("description") or "No detailed experience bullet detected."
        title = first.get("job_title") or "your role"
        tool = skills[0] if skills else "relevant technologies"
        cards.append({
            "section": "Experience",
            "before": before,
            "after": f"Developed and optimized {tool}-based solutions as {title}, improving workflow efficiency by 30% through automation and measurable delivery improvements.",
            "why": "Adds an action verb, technology keyword, ownership, and a quantified result.",
        })
    if projects:
        project = projects[0]
        before = project.get("description") or "Project description is missing."
        title = project.get("title") or "Featured project"
        technologies = project.get("technologies") or skills[:3]
        cards.append({
            "section": "Projects",
            "before": before,
            "after": f"{title} | {', '.join(map(str, technologies))}\nBuilt a production-minded solution that automated a real workflow and delivered a measurable improvement for users.",
            "why": "Connects the project title to its stack, purpose, and outcome for better ATS evidence.",
        })
    cards.append({
        "section": "Skills",
        "before": ", ".join(skills) or "No skills detected.",
        "after": "Languages: " + ", ".join(skills[:5] or ["Python, JavaScript"]) + "\nTools & Frameworks: " + ", ".join(skills[5:10] or ["FastAPI, Git, SQL"]),
        "why": "Groups keywords into ATS-readable categories instead of one undifferentiated list.",
    })
    return {"cards": cards}
