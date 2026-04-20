from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from PIL import Image


ConvertFn = Callable[[Path, Path], None]


def jpg_to_png(src: Path, dst: Path) -> None:
    with Image.open(src) as img:
        img.save(dst, format="PNG")


def png_to_jpg(src: Path, dst: Path) -> None:
    with Image.open(src) as img:
        img.convert("RGB").save(dst, format="JPEG", quality=95)


def copy_content(src: Path, dst: Path) -> None:
    shutil.copy2(src, dst)


@dataclass(frozen=True)
class ConversionPair:
    label: str
    src_ext: str
    dst_ext: str
    fn: ConvertFn


CONVERSIONS: dict[str, ConversionPair] = {
    "JPG → PNG": ConversionPair("JPG → PNG", ".jpg", ".png", jpg_to_png),
    "PNG → JPG": ConversionPair("PNG → JPG", ".png", ".jpg", png_to_jpg),
    "TXT → MD":  ConversionPair("TXT → MD",  ".txt", ".md",  copy_content),
    "MD → TXT":  ConversionPair("MD → TXT",  ".md",  ".txt", copy_content),
}
