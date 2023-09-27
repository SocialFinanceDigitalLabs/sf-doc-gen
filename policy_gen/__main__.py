from pathlib import Path

from .generator import create_pdf

project_root = Path(__file__).parent.parent
logo_path = project_root / "source/_static/logo_white.png"
build_path = project_root / "build"
build_path.mkdir(parents=True, exist_ok=True)


sample_text_v2 = [
    "<b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
    "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old.",
    "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable.",
]

output_filename_v4 = build_path / "policy.pdf"
create_pdf(sample_text_v2, output_filename_v4.as_posix())
