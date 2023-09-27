from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table

from .pdf import PolicyTemplate, getChangeManagementTableStyle, getPolicyStylesheet


def create_pdf(paragraphs, filename):
    # Define a custom document with headers and footers
    doc = PolicyTemplate(filename)

    styles = getPolicyStylesheet()

    Story = [
        Spacer(1, inch),
        Paragraph("Document Title", styles["Title"]),
        Spacer(1, 0.25 * inch),
    ]
    data = [
        ["Version", "Date", "Author", "Changes Made"],
        ["1.0", "25/09/2023", "John Doe", "Initial version"],
    ]
    table = Table(data, colWidths=[1.5 * inch] * 4)
    table.setStyle(getChangeManagementTableStyle())
    Story.append(table)
    Story.append(PageBreak())
    Story.append(Paragraph(" ", styles["Normal"]))  # Some space after the table

    # Adding paragraphs without forced page breaks
    for para_text in paragraphs:
        p = Paragraph(para_text, styles["Paragraph"])
        Story.append(p)

    doc.build(Story)
