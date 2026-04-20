from pathlib import Path

from PIL import Image

from app.converters import CONVERSIONS, copy_content, jpg_to_png, png_to_jpg


class TestJpgToPng:
    def test_output_exists(self, sample_jpg: Path, tmp_path: Path) -> None:
        dst = tmp_path / "out.png"
        jpg_to_png(sample_jpg, dst)
        assert dst.exists()

    def test_output_format_is_png(self, sample_jpg: Path, tmp_path: Path) -> None:
        dst = tmp_path / "out.png"
        jpg_to_png(sample_jpg, dst)
        with Image.open(dst) as img:
            assert img.format == "PNG"

    def test_dimensions_preserved(self, sample_jpg: Path, tmp_path: Path) -> None:
        dst = tmp_path / "out.png"
        jpg_to_png(sample_jpg, dst)
        with Image.open(sample_jpg) as src, Image.open(dst) as out:
            assert src.size == out.size

    def test_source_file_unchanged(self, sample_jpg: Path, tmp_path: Path) -> None:
        original = sample_jpg.read_bytes()
        jpg_to_png(sample_jpg, tmp_path / "out.png")
        assert sample_jpg.read_bytes() == original


class TestPngToJpg:
    def test_output_exists(self, sample_png_rgb: Path, tmp_path: Path) -> None:
        dst = tmp_path / "out.jpg"
        png_to_jpg(sample_png_rgb, dst)
        assert dst.exists()

    def test_output_format_is_jpeg(self, sample_png_rgb: Path, tmp_path: Path) -> None:
        dst = tmp_path / "out.jpg"
        png_to_jpg(sample_png_rgb, dst)
        with Image.open(dst) as img:
            assert img.format == "JPEG"

    def test_dimensions_preserved(self, sample_png_rgb: Path, tmp_path: Path) -> None:
        dst = tmp_path / "out.jpg"
        png_to_jpg(sample_png_rgb, dst)
        with Image.open(sample_png_rgb) as src, Image.open(dst) as out:
            assert src.size == out.size

    def test_rgba_input_converted_to_rgb(self, sample_png_rgba: Path, tmp_path: Path) -> None:
        dst = tmp_path / "out.jpg"
        png_to_jpg(sample_png_rgba, dst)
        assert dst.exists()
        with Image.open(dst) as img:
            assert img.mode == "RGB"

    def test_source_file_unchanged(self, sample_png_rgb: Path, tmp_path: Path) -> None:
        original = sample_png_rgb.read_bytes()
        png_to_jpg(sample_png_rgb, tmp_path / "out.jpg")
        assert sample_png_rgb.read_bytes() == original


class TestCopyContent:
    def test_txt_to_md_content_preserved(self, sample_txt: Path, tmp_path: Path) -> None:
        dst = tmp_path / "out.md"
        original = sample_txt.read_text(encoding="utf-8")
        copy_content(sample_txt, dst)
        assert dst.read_text(encoding="utf-8") == original

    def test_md_to_txt_content_preserved(self, sample_md: Path, tmp_path: Path) -> None:
        dst = tmp_path / "out.txt"
        original = sample_md.read_text(encoding="utf-8")
        copy_content(sample_md, dst)
        assert dst.read_text(encoding="utf-8") == original

    def test_source_file_unchanged(self, sample_txt: Path, tmp_path: Path) -> None:
        original = sample_txt.read_bytes()
        copy_content(sample_txt, tmp_path / "out.md")
        assert sample_txt.read_bytes() == original

    def test_output_file_exists(self, sample_txt: Path, tmp_path: Path) -> None:
        dst = tmp_path / "out.md"
        copy_content(sample_txt, dst)
        assert dst.exists()


class TestConversionsRegistry:
    def test_all_labels_present(self) -> None:
        expected = {"JPG → PNG", "PNG → JPG", "TXT → MD", "MD → TXT"}
        assert set(CONVERSIONS.keys()) == expected

    def test_extensions_start_with_dot(self) -> None:
        for pair in CONVERSIONS.values():
            assert pair.src_ext.startswith(".")
            assert pair.dst_ext.startswith(".")

    def test_src_and_dst_extensions_differ(self) -> None:
        for pair in CONVERSIONS.values():
            assert pair.src_ext != pair.dst_ext

    def test_label_matches_key(self) -> None:
        for key, pair in CONVERSIONS.items():
            assert pair.label == key
