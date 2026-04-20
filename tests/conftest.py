import pytest
from pathlib import Path
from PIL import Image


@pytest.fixture()
def sample_jpg(tmp_path: Path) -> Path:
    path = tmp_path / "sample.jpg"
    Image.new("RGB", (20, 20), color=(200, 100, 50)).save(path, format="JPEG")
    return path


@pytest.fixture()
def sample_png_rgb(tmp_path: Path) -> Path:
    path = tmp_path / "sample_rgb.png"
    Image.new("RGB", (20, 20), color=(50, 100, 200)).save(path, format="PNG")
    return path


@pytest.fixture()
def sample_png_rgba(tmp_path: Path) -> Path:
    path = tmp_path / "sample_rgba.png"
    Image.new("RGBA", (20, 20), color=(50, 100, 200, 128)).save(path, format="PNG")
    return path


@pytest.fixture()
def sample_txt(tmp_path: Path) -> Path:
    path = tmp_path / "sample.txt"
    path.write_text("Hello, World!\nLine 2", encoding="utf-8")
    return path


@pytest.fixture()
def sample_md(tmp_path: Path) -> Path:
    path = tmp_path / "sample.md"
    path.write_text("# Heading\n\n**Bold** text", encoding="utf-8")
    return path
