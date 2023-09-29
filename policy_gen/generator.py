from collections import deque
from pathlib import Path

import frontmatter
import markdown
from bs4 import BeautifulSoup
from reportlab.lib.units import inch
from reportlab.platypus import (
    BulletDrawer,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Spacer,
    Table,
)

from policy_gen.level_numbering import NumberContext

from .pdf import PolicyTemplate, getChangeManagementTableStyle, getPolicyStylesheet


class Grouper:
    def __init__(self, story):
        self.current = []
        self.story = story

    def append(self, item):
        self.current.append(item)

    def flush(self):
        if len(self.current) > 0:
            self.story.append(KeepTogether(self.current))
            self.current = []


def create_pdf(source, filename):
    with open(source) as f:
        post = frontmatter.load(f)

    metadata = post.metadata

    html = markdown.markdown(post.content)
    soup = BeautifulSoup(html, "html.parser")

    # Define a custom document with headers and footers
    doc = PolicyTemplate(filename.as_posix())

    styles = getPolicyStylesheet()

    Story = [
        Spacer(1, inch),
        Paragraph(metadata.get("title", "Unnamed Policy").upper(), styles["Title"]),
        Spacer(1, 0.25 * inch),
    ]

    change_management = metadata.get("changeManagement", None)
    if change_management:
        data = [
            ["Version", "Date", "Summary", "Aproved By"],
        ] + [
            [
                Paragraph(str(r.get("version", ""))),
                Paragraph(str(r.get("date", ""))),
                Paragraph(r.get("summary", "")),
                Paragraph(r.get("approvedBy", "")),
            ]
            for r in change_management
        ]
        table = Table(data, colWidths=[1.75 * inch] * 4)
        table.setStyle(getChangeManagementTableStyle())
        Story.append(table)
        Story.append(PageBreak())

    paragraph_ctx = NumberContext()

    list_numbers = deque()
    current_batch = Grouper(Story)
    for tag in soup:
        if tag.name is None:
            continue

        if tag.name == "h1":
            current_batch.flush()
            heading_text = f"{paragraph_ctx.get_level(1)} {str(tag)}"
            current_batch.append(Paragraph(heading_text, styles["Heading1"]))

        elif tag.name == "ol":
            list_items = []
            for sub_tag in tag.contents:
                if str(sub_tag).strip() == "":
                    continue
                list_items.append(Paragraph(str(sub_tag), style=styles["BodyText"]))
                list_numbers.append(paragraph_ctx.get_level(2))

            current_batch.append(
                ListFlowable(
                    list_items,
                    bulletFormat=lambda x: list_numbers.popleft(),
                    bulletFontSize=12,
                    leftIndent=30,
                )
            )

        elif tag.name == "p":
            p = Paragraph(str(tag), styles["BodyText"])
            current_batch.append(p)

        elif tag.name == "ul":
            list_items = []
            for sub_tag in tag.contents:
                list_items.append(Paragraph(str(sub_tag), style=styles["BodyText"]))
            ul = ListFlowable(list_items, bulletType="bullet")
            current_batch.append(ul)

        else:
            print("Unknown tag: ", tag.name)

    current_batch.flush()
    doc.build(Story)
