import logging
from collections import deque
from pathlib import Path

import frontmatter
import git
import markdown
import yaml
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

logger = logging.getLogger(__name__)


def find_git_root(start_directory: Path) -> Path:
    """
    Find the root directory of the Git repository that contains the specified directory.
    """
    current_directory = start_directory
    while (
        current_directory != current_directory.parent
    ):  # While it's not the root directory
        if (current_directory / ".git").is_dir():
            return current_directory
        current_directory = current_directory.parent
    return None


def is_file_dirty(repo: git.Repo, file_path: Path) -> bool:
    """
    Check if a specific file in the repository has uncommitted changes, either staged or unstaged.
    """
    file_relative_path = file_path.as_posix()

    # Check if the file is untracked
    if file_relative_path in repo.untracked_files:
        return True

    # Check for unstaged changes
    if file_relative_path in [diff.a_path for diff in repo.index.diff(None)]:
        return True

    # Check for staged changes
    if file_relative_path in [diff.a_path for diff in repo.index.diff("HEAD")]:
        return True

    return False


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


def create_pdf(source: Path, filename: Path):
    with open(source) as f:
        post = frontmatter.load(f)

    metadata = post.metadata

    if source.with_suffix(".yaml").exists():
        extra_metadata = yaml.safe_load(source.with_suffix(".yaml").read_text())
        metadata = {**metadata, **extra_metadata}

    repo_path = find_git_root(source.resolve().parent)
    if repo_path:
        try:
            repo = git.Repo(repo_path)
            commits = list(repo.iter_commits(paths=source.as_posix(), max_count=1))
            if commits:
                metadata["git.current"] = commits[0].hexsha
                metadata["git.dirty"] = is_file_dirty(repo, source)
        except:
            logger.exception("Error getting git commit")

    html = markdown.markdown(post.content)
    soup = BeautifulSoup(html, "html.parser")

    # Define a custom document with headers and footers
    doc = PolicyTemplate(filename.as_posix(), metadata=metadata)

    styles = getPolicyStylesheet()

    Story = [
        Spacer(1, inch),
        Paragraph(metadata.get("title", "Unnamed Policy").upper(), styles["Title"]),
        Spacer(1, 0.25 * inch),
    ]

    change_management = metadata.get("changeManagement", None)
    if change_management:
        data = [["Version", "Date", "Summary", "Aproved By"]]
        for ix, revision in enumerate(change_management):
            prev_revision = change_management[ix - 1] if ix > 0 else {}
            version = str(revision.get("version", ""))
            git_sha = revision.get("git_sha")
            if git_sha:
                prev_sha = prev_revision.get("git_sha")
                if prev_sha:
                    link = f"https://github.com/SocialFinanceDigitalLabs/policies/compare/{prev_sha}...{git_sha}"
                else:
                    link = f"https://github.com/SocialFinanceDigitalLabs/policies/commit/{git_sha}"
                version += f"<br/><a href='{link}'>{revision['git_sha'][:7]}</a>"
            date = str(revision.get("date", ""))
            summary = revision.get("summary", "")
            approved_by = revision.get("approvedBy", "")
            data.append(
                [
                    Paragraph(version),
                    Paragraph(date),
                    Paragraph(summary),
                    Paragraph(approved_by),
                ]
            )

        page_width = doc.pagesize[0] - doc.leftMargin - doc.rightMargin

        table = Table(data, colWidths=[page_width / 4] * 4)
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
