from pathlib import Path

from app.scanner import scan_files


class TestScanFiles:
    def test_empty_directory_returns_empty(self, tmp_path: Path) -> None:
        assert scan_files([tmp_path], ".jpg") == []

    def test_finds_matching_files_in_dir(self, tmp_path: Path) -> None:
        (tmp_path / "a.jpg").touch()
        (tmp_path / "b.jpg").touch()
        result = scan_files([tmp_path], ".jpg")
        assert len(result) == 2

    def test_ignores_other_extensions(self, tmp_path: Path) -> None:
        (tmp_path / "a.jpg").touch()
        (tmp_path / "b.png").touch()
        result = scan_files([tmp_path], ".jpg")
        assert len(result) == 1
        assert result[0].name == "a.jpg"

    def test_recursive_finds_nested_files(self, tmp_path: Path) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "a.jpg").touch()
        (sub / "b.jpg").touch()
        result = scan_files([tmp_path], ".jpg", recursive=True)
        assert len(result) == 2

    def test_non_recursive_skips_subdirs(self, tmp_path: Path) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "a.jpg").touch()
        (sub / "b.jpg").touch()
        result = scan_files([tmp_path], ".jpg", recursive=False)
        assert len(result) == 1
        assert result[0].name == "a.jpg"

    def test_direct_file_path_included(self, tmp_path: Path) -> None:
        f = tmp_path / "a.jpg"
        f.touch()
        result = scan_files([f], ".jpg")
        assert result == [f]

    def test_direct_file_wrong_extension_excluded(self, tmp_path: Path) -> None:
        f = tmp_path / "a.png"
        f.touch()
        result = scan_files([f], ".jpg")
        assert result == []

    def test_multiple_directories(self, tmp_path: Path) -> None:
        d1 = tmp_path / "d1"
        d2 = tmp_path / "d2"
        d1.mkdir()
        d2.mkdir()
        (d1 / "a.txt").touch()
        (d2 / "b.txt").touch()
        result = scan_files([d1, d2], ".txt")
        assert len(result) == 2

    def test_mixed_files_and_dirs(self, tmp_path: Path) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        direct_file = tmp_path / "direct.jpg"
        direct_file.touch()
        (sub / "nested.jpg").touch()
        result = scan_files([direct_file, sub], ".jpg")
        assert len(result) == 2

    def test_empty_paths_list_returns_empty(self) -> None:
        assert scan_files([], ".jpg") == []
