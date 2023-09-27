from pathlib import Path

import frontmatter
import markdown
from bs4 import BeautifulSoup
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Spacer,
    Table,
)

from .pdf import PolicyTemplate, getChangeManagementTableStyle, getPolicyStylesheet


def create_pdf(source, filename):
    with open(source) as f:
        post = frontmatter.load(f)

    metadata = post.metadata

    html = markdown.markdown(post.content)
    soup = BeautifulSoup(html, "html.parser")

    # Define a custom document with headers and footers
    doc = PolicyTemplate(filename)

    styles = getPolicyStylesheet()

    Story = [
        Spacer(1, inch),
        Paragraph(metadata["title"], styles["Title"]),
        Spacer(1, 0.25 * inch),
    ]

    change_management = metadata.get("changeManagement", None)
    if change_management:
        data = [
            ["Version", "Date", "Summary", "Aproved By"],
        ] + [
            [
                Paragraph(f"{r['version']}"),
                Paragraph(f"{r['date']}"),
                Paragraph(r["summary"]),
                Paragraph(r["approvedBy"]),
            ]
            for r in change_management
        ]
        table = Table(data, colWidths=[1.5 * inch] * 4)
        table.setStyle(getChangeManagementTableStyle())
        Story.append(table)
        Story.append(PageBreak())

    # Adding paragraphs without forced page breaks
    for tag in soup:
        if tag.name == "h1":
            Story.append(Paragraph(str(tag), styles["Heading1"]))
        elif tag.name == "p":
            print(str(tag))
            p = Paragraph(str(tag), styles["BodyText"])
            Story.append(p)
        elif tag.name == "ul":
            list_items = []
            for sub_tag in tag.contents:
                list_items.append(
                    ListItem(Paragraph(str(sub_tag), style=styles["BodyText"]))
                )
            ul = ListFlowable(list_items, bulletType="bullet")
            Story.append(ul)
    doc.build(Story)
