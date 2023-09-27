from pathlib import Path

from .generator import create_pdf

project_root = Path(__file__).parent.parent
build_path = project_root / "build"
build_path.mkdir(parents=True, exist_ok=True)

output_filename_v4 = build_path / "policy.pdf"
create_pdf(project_root / "source/policies/laptop.md", output_filename_v4.as_posix())
