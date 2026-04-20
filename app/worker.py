from __future__ import annotations

import threading
from pathlib import Path
from typing import Optional

from PyQt5.QtCore import QThread, pyqtSignal

from app.converters import ConversionPair


class ConversionWorker(QThread):
    progress = pyqtSignal(int)          # 0–100
    log_message = pyqtSignal(str)
    finished = pyqtSignal(int, int)     # success_count, fail_count

    def __init__(
        self,
        files: list[Path],
        pair: ConversionPair,
        output_dir: Optional[Path],
        overwrite: bool,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._files = files
        self._pair = pair
        self._output_dir = output_dir
        self._overwrite = overwrite
        self._cancel = threading.Event()

    def cancel(self) -> None:
        self._cancel.set()

    def run(self) -> None:
        total = len(self._files)
        success = 0
        failed = 0

        for i, src in enumerate(self._files):
            if self._cancel.is_set():
                self.log_message.emit("Conversion cancelled by user.")
                break

            dest_dir = self._output_dir if self._output_dir else src.parent
            dst = dest_dir / (src.stem + self._pair.dst_ext)

            if dst.exists() and not self._overwrite:
                self.log_message.emit(f"[SKIP]  {src.name}  (destination exists)")
                failed += 1
            else:
                try:
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    self._pair.fn(src, dst)
                    self.log_message.emit(f"[OK]    {src.name}  →  {dst.name}")
                    success += 1
                except Exception as exc:
                    self.log_message.emit(f"[ERROR] {src.name}  —  {exc}")
                    failed += 1

            self.progress.emit(round((i + 1) / total * 100))

        self.finished.emit(success, failed)
