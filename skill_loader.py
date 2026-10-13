
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
SKILLS_DIR = BASE_DIR / "skills"


def load_skills():
    """Discover and load available SKILL.md files."""
    skills = []

    for skill_file in SKILLS_DIR.glob("*/SKILL.md"):
        content = skill_file.read_text(encoding="utf-8")

        # Read name and description from YAML frontmatter
        frontmatter = re.match(
            r"\A---\s*\n(.*?)\n---",
            content,
            re.DOTALL,
        )

        if not frontmatter:
            continue

        metadata = frontmatter.group(1)

        name_match = re.search(
            r"(?m)^name:\s*(.+)$", metadata
        )
        description_match = re.search(
            r"(?m)^description:\s*(.+)$", metadata
        )

        if not name_match or not description_match:
            continue

        skills.append({
            "name": name_match.group(1).strip().strip("\"'"),
            "description": description_match.group(1).strip().strip("\"'"),
            "instructions": content,
        })

    return skills
