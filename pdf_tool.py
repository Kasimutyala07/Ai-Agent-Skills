
from pathlib import Path
from datetime import datetime
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)


def create_pdf(title, sections):
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    safe_title = re.sub(
        r"[^A-Za-z0-9_-]+", "_", title
    ).strip("_")[:40] or "Report"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{safe_title}_{timestamp}.pdf"

    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    story = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 18),
    ]

    for heading, content in sections.items():
        story.append(Paragraph(str(heading), styles["Heading2"]))
        story.append(
            Paragraph(
                str(content).replace("&", "&amp;").replace(
                    "<", "&lt;"
                ).replace(">", "&gt;").replace("\n", "<br/>"),
                styles["BodyText"],
            )
        )
        story.append(Spacer(1, 12))

    doc.build(story)
    return str(path)
