import requests
from packaging.version import Version
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QStatusBar, QMessageBox, QLabel

VERSION = "0.0.1"
VERSION_URL = "https://raw.githubusercontent.com/elliottsneath/app-version-control/main/version.json"
VERSION_ID_NUMBER = "01"
APP_NAME = "Pokemon Draft Searcher"

class VersionControl:
    def __init__(self, version_action: QAction, status_bar: QStatusBar):
        self.version_action: QAction = version_action
        self.status_bar: QStatusBar = status_bar
        self.version_status_label = QLabel()
        self.status_bar.addPermanentWidget(self.version_status_label)

        self.update_menu()
        self.check_for_updates()

    def check_for_updates(self):
        all_version_data = self.fetch_update_info()

        if not all_version_data:
            return
        
        version_data = all_version_data.get(VERSION_ID_NUMBER, {})
        latest_version_str = version_data.get("version", "0.0.0")
        latest_version_date = version_data.get(f"release_date", "Unknown date")

        current_version = Version(VERSION)
        latest_version = Version(latest_version_str)

        if latest_version > current_version:
            update_message = f"Good news!\nA new version of {APP_NAME} is available! (v{latest_version_str}, released on {latest_version_date})\n\nPlease visit the Sharepoint to download the latest version."
            QMessageBox.information(None, "Update Available", update_message)
            self.update_status(f"New version available: v{latest_version_str}, released on {latest_version_date}")
        else:
            self.update_status(f"You are using the latest version of {APP_NAME}.")

    def fetch_update_info(self):
        try:
            response = requests.get(VERSION_URL, timeout=5)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            print("Failed to fetch update info:", e)
            self.update_status("Failed to check for updates.")
            return

    def update_menu(self):
        self.version_action.setText(f"Version {VERSION}")

    def update_status(self, message: str):
        self.version_status_label.setText(f"{message}  ")
