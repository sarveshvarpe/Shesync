from io import BytesIO
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from app.models.cycle import Cycle


def generate_health_report(db, user, summary_data):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    elements = []

    # ===============================
    # TITLE
    # ===============================

    elements.append(Paragraph("SheSync AI Health Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(f"User: {user.name}", styles["Normal"])
    )

    elements.append(
        Paragraph(
            f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # ===============================
    # HEALTH SUMMARY
    # ===============================

    elements.append(Paragraph("Health Summary", styles["Heading2"]))

    elements.append(
        Paragraph(
            f"Cycle Health Score: {summary_data.get('cycle_health_score')}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Hormonal Stability: {summary_data.get('hormonal_stability_index')}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Fertility Score: {summary_data.get('fertility_score')}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"PCOS Risk Level: {summary_data.get('pcos_risk_level')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # ===============================
    # CYCLE HISTORY
    # ===============================

    cycles = db.query(Cycle).filter(
        Cycle.user_id == user.id
    ).order_by(Cycle.start_date.desc()).all()

    table_data = [["Start Date", "End Date"]]

    for c in cycles:
        table_data.append([
            str(c.start_date),
            str(c.end_date) if c.end_date else "Active"
        ])

    table = Table(table_data)

    table.setStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightpink),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey)
    ])

    elements.append(Paragraph("Cycle History", styles["Heading2"]))
    elements.append(table)

    elements.append(Spacer(1, 20))

    # ===============================
    # RECOMMENDATIONS
    # ===============================

    elements.append(Paragraph("AI Recommendations", styles["Heading2"]))

    recs = summary_data.get("recommendations", [])

    for r in recs:
        elements.append(Paragraph(f"- {r}", styles["Normal"]))

    doc.build(elements)

    buffer.seek(0)

    return buffer