"""Handles the settings page: pool selector, Pokémon list apply/export/import/reset."""

from __future__ import annotations
import json
import os
import re
import tempfile
import urllib.request
from typing import TYPE_CHECKING

import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QDialog, QFileDialog, QInputDialog, QMessageBox, QProgressDialog,
)
from PySide6.QtCore import Qt

from assets.ui.import_popup_ui import Ui_Form
from assets.ui.pokemon_list_item import SettingsPokemonListItem
from common.draft_format import DraftFormat
from common.handlers.draft_parser import normalise_pokemon, parse_draft_board, UNWANTED_STRINGS
from common.widget_groups import SettingsWidgets

if TYPE_CHECKING:
    from main import MainWindow


class SettingsHandler:
    def __init__(self, window: MainWindow, widgets: SettingsWidgets):
        self.w = window
        self.wg = widgets
        self._connect_signals()

    _FORMAT_ORDER = [
        DraftFormat.SV,
        DraftFormat.NATDEX,
        DraftFormat.CHAMPIONS,
        DraftFormat.CHAMPIONS_NATDEX,
    ]

    def _connect_signals(self) -> None:
        self.wg.apply_button.clicked.connect(self.apply_pokemon_list)
        self.wg.search_bar.textChanged.connect(self.search_settings)
        self.wg.export_button.clicked.connect(self.export_pokemon_list)
        self.wg.import_button.clicked.connect(self.import_pokemon_list)
        self.wg.reset_button.clicked.connect(self.reset_pokemon_list)
        self.wg.refresh_button.clicked.connect(self.sync_from_sheet)
        self.wg.refresh_button.setEnabled(bool(self.w.sheet_url))
        self.populate_pool_combobox()
        self._init_format_combo()
        self.wg.pool_combo.currentIndexChanged.connect(self.change_pool)

    # ── pool ───────────────────────────────────────────────────────────────

    def populate_pool_combobox(self) -> None:
        self.wg.pool_combo.blockSignals(True)
        self.wg.pool_combo.clear()
        self.wg.pool_combo.addItem("None")
        for pool in range(1, self.w.draft_pools + 1):
            self.wg.pool_combo.addItem(f"P{pool}")
        idx = self.w.pool if (self.w.pool and self.w.pool <= self.w.draft_pools) else 0
        self.wg.pool_combo.setCurrentIndex(idx)
        self.wg.pool_combo.blockSignals(False)

    def change_pool(self, index: int) -> None:
        self.w.pool = index if index > 0 else None
        print(f"[Settings] pool changed → {self.w.pool}")
        self.w.data_handler.save_config()
        self.w.data_handler.refresh_draft_status()
        self.w.pokemon_list_handler.update()

    # ── format ─────────────────────────────────────────────────────────────

    def _init_format_combo(self) -> None:
        try:
            idx = self._FORMAT_ORDER.index(self.w.draft_format)
        except ValueError:
            idx = len(self._FORMAT_ORDER) - 1
        self.wg.format_combo.blockSignals(True)
        self.wg.format_combo.setCurrentIndex(idx)
        self.wg.format_combo.blockSignals(False)
        self.wg.format_combo.currentIndexChanged.connect(self.change_format)

    def change_format(self, index: int) -> None:
        prev = self.w.draft_format
        try:
            self.w.draft_format = self._FORMAT_ORDER[index]
        except IndexError:
            self.w.draft_format = DraftFormat.CHAMPIONS_NATDEX
        print(f"[Settings] format changed {prev.value} → {self.w.draft_format.value}")
        self.w.data_handler.save_config()
        self.w.all_moves = {m for p in self.w.master_list for m in p.moves_for(self.w.draft_format)}
        print(f"[Settings] all_moves rebuilt: {len(self.w.all_moves)} moves")
        self.w.pokemon_list_handler.filter_completer()
        self.w.pokemon_list_handler.update()
        self.w.draft_handler.analyse_team_matchups()

    # ── apply ──────────────────────────────────────────────────────────────

    def apply_pokemon_list(self, popup: bool = True) -> None:
        if popup:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Confirm Apply")
            msg.setText("Are you sure you want to apply the changes to the Pokémon list?")
            msg.setInformativeText(
                "This will overwrite the selected Pokémon list and "
                "changes will remain after restarting the app."
            )
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            if msg.exec() == QMessageBox.Cancel:
                return

        self.w.selected_pokemon = []
        for i in range(self.wg.pokemon_list_widget.count()):
            item = self.wg.pokemon_list_widget.item(i)
            widget: SettingsPokemonListItem = self.wg.pokemon_list_widget.itemWidget(item)
            if widget.checkbox.isChecked():
                self.w.selected_pokemon.append(widget.name_label.text())

        print(f"[Settings] apply — {len(self.w.selected_pokemon)} pokemon selected")
        try:
            self.w.data_handler.save_selected_pokemon()
        except Exception as e:
            print(f"[Settings] Error saving selected Pokémon: {e}")

        self.w.pokemon_list_handler.reset_state()
        self.w.data_handler.load_pokemon_data(init=False)
        self.w.pokemon_list_handler.update()

    # ── search ─────────────────────────────────────────────────────────────

    def search_settings(self, text: str) -> None:
        search_text = text.lower()
        for i in range(self.wg.pokemon_list_widget.count()):
            item = self.wg.pokemon_list_widget.item(i)
            widget = self.wg.pokemon_list_widget.itemWidget(item)
            item.setHidden(search_text not in widget.name_label.text().lower())

    # ── export ─────────────────────────────────────────────────────────────

    def export_pokemon_list(self) -> None:
        self.apply_pokemon_list(popup=False)
        file_path, _ = QFileDialog.getSaveFileName(
            self.w, "Export Pokémon List", "",
            "Pokémon List Files (*.pkmnlist);;JSON Files (*.json);;All Files (*)"
        )
        if not file_path:
            return
        if not file_path.endswith(".pkmnlist"):
            file_path += ".pkmnlist"
        try:
            with open(file_path, "w") as f:
                json.dump(self.w.data_handler.selected_pokemon_json(), f, indent=4)
        except Exception as e:
            QMessageBox.critical(self.w, "Export Error", f"Failed to export Pokémon list:\n{e}")

    # ── import ─────────────────────────────────────────────────────────────

    def import_pokemon_list(self) -> None:
        dialog = QDialog(self.w)
        ui = Ui_Form()
        ui.setupUi(dialog)

        def connect_to_sheet():
            url, ok = QInputDialog.getText(
                self.w, "Connect to Google Sheet", "Paste the Google Sheets URL:",
                text=self.w.sheet_url,
            )
            if not ok:
                return
            self.w.sheet_url = url.strip()
            self.w.data_handler.save_config()
            self.wg.refresh_button.setEnabled(bool(self.w.sheet_url))
            dialog.accept()
            if self.w.sheet_url:
                self.sync_from_sheet()

        def import_from_file():
            file_path, _ = QFileDialog.getOpenFileName(
                self.w, "Import Pokémon List", "",
                "Pokémon List Files (*.pkmnlist);;JSON Files (*.json);;All Files (*)"
            )
            if not file_path:
                return
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                selected = data.get("selected_pokemon")
                if not isinstance(selected, list):
                    raise ValueError("Invalid file format: 'selected_pokemon' not found or not a list.")
                if "draft_board" in data:
                    self.w.draft_board = data["draft_board"]
                    self.w.draft_pools = data.get("draft_pools", 0)
                    self.populate_pool_combobox()
                self._apply_imported_list(selected, dialog)
                print(f"[Settings] imported from file — {len(selected)} pokemon")
                QMessageBox.information(self.w, "Import Successful", "Pokémon list imported successfully.")
            except Exception as e:
                print(f"[Settings] import from file failed: {e}")
                QMessageBox.critical(self.w, "Import Error", f"Failed to import Pokémon list:\n{e}")

        def import_from_doc():
            file_path, _ = QFileDialog.getOpenFileName(
                self.w, "Draft Board Excel", "",
                "Microsoft Excel Worksheet (*.xlsx);;All Files (*)"
            )
            if not file_path:
                return
            try:
                xls = pd.ExcelFile(file_path, engine='openpyxl')
                target_sheet = self._pick_sheet(xls)
                if target_sheet is None:
                    return

                df = pd.read_excel(xls, sheet_name=target_sheet, engine='openpyxl')
                raw_list = df.astype(str).values.flatten().tolist()

                if any(isinstance(v, str) and v.strip().lower() == "banned" for v in df.iloc[:, 1]):
                    banned_set = {
                        v for v in df.iloc[:, 2]
                        if isinstance(v, str) and v.strip() and v.strip().lower() != "banned"
                    }
                    raw_list = [v for v in raw_list if v not in banned_set]

                imported_list, excluded_list, seen = [], [], set()
                for raw in raw_list:
                    normalised = normalise_pokemon(raw)
                    if (normalised and normalised not in UNWANTED_STRINGS
                            and normalised in self.w.pokedex and normalised not in seen):
                        imported_list.append(normalised)
                    elif normalised and normalised not in UNWANTED_STRINGS and normalised not in seen:
                        excluded_list.append(raw)
                    seen.add(normalised)

                if excluded_list:
                    QMessageBox.warning(
                        self.w, "Excluded Pokémon",
                        f"The following Pokémon failed to be normalised and imported:\n"
                        f"{', '.join(excluded_list)}"
                    )

                draft_board, draft_pools = parse_draft_board(xls, target_sheet, self.w.pokedex)
                self.w.draft_board = draft_board
                self.w.draft_pools = draft_pools

                if draft_pools and not (self.w.pool and self.w.pool <= draft_pools):
                    pool_names = [f"P{p}" for p in range(1, draft_pools + 1)]
                    choice, ok = QInputDialog.getItem(
                        self.w, "Draft Pool", "Which pool are you in?", pool_names, 0, False
                    )
                    self.w.pool = pool_names.index(choice) + 1 if ok else None

                self.w.data_handler.save_config()
                self.populate_pool_combobox()
                self._apply_imported_list(imported_list, dialog)
                self.w.draft_handler.record_import()
                print(f"[Settings] imported from Excel — {len(imported_list)} pokemon, {draft_pools} pools, {len(excluded_list)} excluded")
                QMessageBox.information(self.w, "Import Successful", "Pokémon list imported successfully.")
            except Exception as e:
                print(f"[Settings] import from Excel failed: {e}")
                QMessageBox.critical(
                    self.w, "Import Error",
                    f"Failed to import Pokémon list from Excel:\n{e}"
                )

        ui.fromGoogleSheetButton.clicked.connect(connect_to_sheet)
        ui.fromFileButton.clicked.connect(import_from_file)
        ui.fromExcelButton.clicked.connect(import_from_doc)
        dialog.exec()

    def _apply_imported_list(self, selected: list[str], dialog: QDialog | None = None) -> None:
        self.w.selected_pokemon = selected
        for widget in self.wg.pokemon_list_widget.findChildren(SettingsPokemonListItem):
            widget.checkbox.setChecked(widget.name_label.text() in selected)
        self.w.data_handler.save_selected_pokemon()
        self.w.pokemon_list_handler.reset_state()
        self.w.data_handler.load_pokemon_data(init=False)
        self.w.pokemon_list_handler.update()
        if dialog is not None:
            dialog.accept()

    # ── sheet sync ─────────────────────────────────────────────────────────

    def _pick_sheet(self, xls: "pd.ExcelFile", silent: bool = False) -> "str | None":
        for name in ("Draft Board", "Board"):
            if name in xls.sheet_names:
                return name
        if silent:
            return None
        choice, ok = QInputDialog.getItem(
            self.w, "Select Sheet",
            "No 'Draft Board' sheet found. Which sheet is the draft board?",
            xls.sheet_names, 0, False,
        )
        return choice if ok else None

    def sync_from_sheet(self, silent: bool = False) -> None:
        if not self.w.sheet_url:
            return
        match = re.search(r'/spreadsheets/d/([^/]+)', self.w.sheet_url)
        if not match:
            if not silent:
                QMessageBox.critical(self.w, "Sync Error", "Could not parse a Google Sheets ID from the URL.")
            return
        sheet_id = match.group(1)
        export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
        tmp_path = None

        progress = QProgressDialog("Connecting...", None, 0, 100, self.w)
        progress.setWindowTitle("Syncing")
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        QApplication.processEvents()

        self.w.setEnabled(False)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents()
        try:
            progress.setLabelText("Downloading sheet...")
            progress.setValue(5)
            QApplication.processEvents()

            with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
                tmp_path = tmp.name
            urllib.request.urlretrieve(export_url, tmp_path)

            progress.setLabelText("Reading spreadsheet...")
            progress.setValue(45)
            QApplication.processEvents()

            xls = pd.ExcelFile(tmp_path, engine='openpyxl')
            target_sheet = self._pick_sheet(xls, silent=silent)
            if target_sheet is None:
                return

            progress.setValue(55)
            QApplication.processEvents()

            df = pd.read_excel(xls, sheet_name=target_sheet, engine='openpyxl')
            raw_list = df.astype(str).values.flatten().tolist()

            if any(isinstance(v, str) and v.strip().lower() == "banned" for v in df.iloc[:, 1]):
                banned_set = {
                    v for v in df.iloc[:, 2]
                    if isinstance(v, str) and v.strip() and v.strip().lower() != "banned"
                }
                raw_list = [v for v in raw_list if v not in banned_set]

            progress.setLabelText("Normalising Pokémon...")
            progress.setValue(65)
            QApplication.processEvents()

            imported_list, excluded_list, seen = [], [], set()
            for raw in raw_list:
                normalised = normalise_pokemon(raw)
                if (normalised and normalised not in UNWANTED_STRINGS
                        and normalised in self.w.pokedex and normalised not in seen):
                    imported_list.append(normalised)
                elif normalised and normalised not in UNWANTED_STRINGS and normalised not in seen:
                    excluded_list.append(raw)
                seen.add(normalised)

            if excluded_list and not silent:
                QMessageBox.warning(
                    self.w, "Excluded Pokémon",
                    f"The following Pokémon failed to be normalised and imported:\n"
                    f"{', '.join(excluded_list)}"
                )

            progress.setLabelText("Parsing draft board...")
            progress.setValue(78)
            QApplication.processEvents()

            draft_board, draft_pools = parse_draft_board(xls, target_sheet, self.w.pokedex)
            self.w.draft_board = draft_board
            self.w.draft_pools = draft_pools

            if not silent and draft_pools and not (self.w.pool and self.w.pool <= draft_pools):
                pool_names = [f"P{p}" for p in range(1, draft_pools + 1)]
                choice, ok = QInputDialog.getItem(
                    self.w, "Draft Pool", "Which pool are you in?", pool_names, 0, False
                )
                self.w.pool = pool_names.index(choice) + 1 if ok else None

            progress.setLabelText("Applying...")
            progress.setValue(88)
            QApplication.processEvents()

            self.w.data_handler.save_config()
            self.populate_pool_combobox()
            self._apply_imported_list(imported_list)
            self.w.draft_handler.record_import()

            progress.setValue(100)
            QApplication.processEvents()

            print(f"[Settings] sheet sync complete — {len(imported_list)} pokemon, {draft_pools} pools, {len(excluded_list)} excluded")
            if not silent:
                QMessageBox.information(self.w, "Sync Successful", "Pokémon list synced from Google Sheets.")
        except Exception as e:
            print(f"[Settings] sheet sync failed: {e}")
            if not silent:
                QMessageBox.critical(self.w, "Sync Error", f"Failed to sync from Google Sheets:\n{e}")
        finally:
            progress.close()
            QApplication.restoreOverrideCursor()
            self.w.setEnabled(True)
            if tmp_path:
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    # ── reset ──────────────────────────────────────────────────────────────

    def reset_pokemon_list(self) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Confirm Reset")
        msg.setText("Are you sure you want to reset the Pokémon list?")
        msg.setInformativeText(
            "This will clear any previous selections and mark the entire Pokédex as available."
        )
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        if msg.exec() == QMessageBox.Cancel:
            return

        for i in range(self.wg.pokemon_list_widget.count()):
            item = self.wg.pokemon_list_widget.item(i)
            widget = self.wg.pokemon_list_widget.itemWidget(item)
            if widget and hasattr(widget, "checkbox"):
                widget.checkbox.setChecked(True)

        self.w.selected_pokemon = list(self.w.pokedex)
        self.w.data_handler.save_selected_pokemon()
        self.w.pokemon_list_handler.reset_state()
        self.w.data_handler.load_pokemon_data(init=False)
        self.w.pokemon_list_handler.update()
