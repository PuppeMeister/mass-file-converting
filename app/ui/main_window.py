from __future__ import annotations

from pathlib import Path
from typing import Optional

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.converters import CONVERSIONS, ConversionPair
from app.scanner import scan_files
from app.worker import ConversionWorker


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._selected_paths: list[Path] = []
        self._output_dir: Optional[Path] = None
        self._worker: Optional[ConversionWorker] = None
        self._setup_ui()

    # ------------------------------------------------------------------ setup

    def _setup_ui(self) -> None:
        self.setWindowTitle("Mass File Converter")
        self.setMinimumSize(720, 600)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(10)
        root.setContentsMargins(16, 16, 16, 16)

        root.addWidget(self._make_source_group())
        root.addWidget(self._make_options_group())
        root.addLayout(self._make_action_row())
        root.addWidget(self._make_log_group(), stretch=1)

    # ------------------------------------------------------------ source group

    def _make_source_group(self) -> QGroupBox:
        group = QGroupBox("Source")
        vbox = QVBoxLayout(group)

        mode_row = QHBoxLayout()
        self._radio_folder = QRadioButton("Folder")
        self._radio_files = QRadioButton("Individual files")
        self._radio_folder.setChecked(True)
        mode_btn_group = QButtonGroup(self)
        mode_btn_group.addButton(self._radio_folder)
        mode_btn_group.addButton(self._radio_files)
        self._radio_folder.toggled.connect(self._on_source_mode_toggled)
        mode_row.addWidget(self._radio_folder)
        mode_row.addWidget(self._radio_files)
        mode_row.addStretch()
        vbox.addLayout(mode_row)

        browse_row = QHBoxLayout()
        self._btn_browse_src = QPushButton("Browse…")
        self._btn_browse_src.setFixedWidth(90)
        self._btn_browse_src.clicked.connect(self._browse_source)
        self._lbl_source = QLabel("No source selected.")
        self._lbl_source.setWordWrap(True)
        browse_row.addWidget(self._btn_browse_src)
        browse_row.addWidget(self._lbl_source, stretch=1)
        vbox.addLayout(browse_row)

        self._chk_recursive = QCheckBox("Include subfolders")
        self._chk_recursive.setChecked(True)
        self._chk_recursive.stateChanged.connect(self._refresh_count)
        vbox.addWidget(self._chk_recursive)

        return group

    # ---------------------------------------------------------- options group

    def _make_options_group(self) -> QGroupBox:
        group = QGroupBox("Conversion Settings")
        vbox = QVBoxLayout(group)

        type_row = QHBoxLayout()
        type_row.addWidget(QLabel("Convert:"))
        self._combo = QComboBox()
        for label in CONVERSIONS:
            self._combo.addItem(label)
        self._combo.currentIndexChanged.connect(self._on_conversion_changed)
        type_row.addWidget(self._combo)
        type_row.addStretch()
        vbox.addLayout(type_row)

        out_row = QHBoxLayout()
        self._radio_out_same = QRadioButton("Same folder as source")
        self._radio_out_custom = QRadioButton("Custom output folder:")
        self._radio_out_same.setChecked(True)
        out_btn_group = QButtonGroup(self)
        out_btn_group.addButton(self._radio_out_same)
        out_btn_group.addButton(self._radio_out_custom)
        self._radio_out_custom.toggled.connect(self._on_out_mode_toggled)
        self._btn_browse_out = QPushButton("Browse…")
        self._btn_browse_out.setFixedWidth(90)
        self._btn_browse_out.setEnabled(False)
        self._btn_browse_out.clicked.connect(self._browse_output)
        self._lbl_out = QLabel("—")
        self._lbl_out.setWordWrap(True)
        out_row.addWidget(self._radio_out_same)
        out_row.addWidget(self._radio_out_custom)
        out_row.addWidget(self._btn_browse_out)
        out_row.addWidget(self._lbl_out, stretch=1)
        vbox.addLayout(out_row)

        self._chk_overwrite = QCheckBox("Overwrite existing files")
        vbox.addWidget(self._chk_overwrite)

        return group

    # ----------------------------------------------------------- action row

    def _make_action_row(self) -> QHBoxLayout:
        hbox = QHBoxLayout()

        self._btn_convert = QPushButton("Convert  (0 files found)")
        self._btn_convert.setFixedHeight(36)
        self._btn_convert.setEnabled(False)
        self._btn_convert.clicked.connect(self._start_conversion)

        self._btn_cancel = QPushButton("Cancel")
        self._btn_cancel.setFixedHeight(36)
        self._btn_cancel.setFixedWidth(80)
        self._btn_cancel.setEnabled(False)
        self._btn_cancel.clicked.connect(self._cancel_conversion)

        self._progress = QProgressBar()
        self._progress.setValue(0)

        hbox.addWidget(self._btn_convert, stretch=2)
        hbox.addWidget(self._btn_cancel)
        hbox.addWidget(self._progress, stretch=3)
        return hbox

    # ------------------------------------------------------------- log group

    def _make_log_group(self) -> QGroupBox:
        group = QGroupBox("Log")
        vbox = QVBoxLayout(group)

        self._log = QTextEdit()
        self._log.setReadOnly(True)
        mono = QFont("Consolas", 9)
        mono.setStyleHint(QFont.Monospace)
        self._log.setFont(mono)
        vbox.addWidget(self._log)

        btn_clear = QPushButton("Clear")
        btn_clear.setFixedWidth(60)
        btn_clear.clicked.connect(self._log.clear)
        clear_row = QHBoxLayout()
        clear_row.addStretch()
        clear_row.addWidget(btn_clear)
        vbox.addLayout(clear_row)

        return group

    # --------------------------------------------------------------- slots

    def _on_source_mode_toggled(self, folder_checked: bool) -> None:
        self._chk_recursive.setEnabled(folder_checked)
        self._selected_paths.clear()
        self._lbl_source.setText("No source selected.")
        self._refresh_count()

    def _on_out_mode_toggled(self, custom_checked: bool) -> None:
        self._btn_browse_out.setEnabled(custom_checked)
        if not custom_checked:
            self._output_dir = None
            self._lbl_out.setText("—")

    def _on_conversion_changed(self) -> None:
        if self._radio_files.isChecked() and self._selected_paths:
            self._selected_paths.clear()
            self._lbl_source.setText(
                "No source selected. (Conversion type changed — please re-select files.)"
            )
        self._refresh_count()

    def _browse_source(self) -> None:
        if self._radio_folder.isChecked():
            folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
            if folder:
                self._selected_paths = [Path(folder)]
                self._lbl_source.setText(folder)
        else:
            pair = self._current_pair()
            files, _ = QFileDialog.getOpenFileNames(
                self,
                "Select Files",
                "",
                f"Supported (*{pair.src_ext});;All files (*.*)",
            )
            if files:
                self._selected_paths = [Path(f) for f in files]
                self._lbl_source.setText(f"{len(files)} file(s) selected")
        self._refresh_count()

    def _browse_output(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self._output_dir = Path(folder)
            self._lbl_out.setText(folder)

    def _current_pair(self) -> ConversionPair:
        return CONVERSIONS[self._combo.currentText()]

    def _matched_files(self) -> list[Path]:
        if not self._selected_paths:
            return []
        pair = self._current_pair()
        recursive = self._chk_recursive.isChecked() and self._radio_folder.isChecked()
        return scan_files(self._selected_paths, pair.src_ext, recursive)

    def _refresh_count(self) -> None:
        count = len(self._matched_files())
        suffix = "s" if count != 1 else ""
        self._btn_convert.setText(f"Convert  ({count} file{suffix} found)")
        self._btn_convert.setEnabled(count > 0)

    def _start_conversion(self) -> None:
        files = self._matched_files()
        if not files:
            return

        pair = self._current_pair()
        output_dir = self._output_dir if self._radio_out_custom.isChecked() else None

        self._set_busy(True)
        self._progress.setValue(0)
        self._log.clear()
        self._log.append(f"Starting — {len(files)} file(s)  [{pair.label}]\n")

        self._worker = ConversionWorker(
            files=files,
            pair=pair,
            output_dir=output_dir,
            overwrite=self._chk_overwrite.isChecked(),
        )
        self._worker.progress.connect(self._progress.setValue)
        self._worker.log_message.connect(self._log.append)
        self._worker.finished.connect(self._on_finished)
        self._worker.start()

    def _cancel_conversion(self) -> None:
        if self._worker and self._worker.isRunning():
            self._worker.cancel()

    def _on_finished(self, success: int, failed: int) -> None:
        self._set_busy(False)
        self._log.append(f"\nFinished — {success} succeeded, {failed} skipped/failed.")

    def _set_busy(self, busy: bool) -> None:
        self._btn_convert.setEnabled(not busy)
        self._btn_cancel.setEnabled(busy)
        self._btn_browse_src.setEnabled(not busy)
        self._radio_folder.setEnabled(not busy)
        self._radio_files.setEnabled(not busy)
        self._combo.setEnabled(not busy)
        folder_mode = self._radio_folder.isChecked()
        self._chk_recursive.setEnabled(not busy and folder_mode)
