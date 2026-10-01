from PySide6.QtCore import QMetaObject, Qt
from PySide6.QtWidgets import (
    QDialogButtonBox, QTextBrowser, QVBoxLayout,
)

_HELP_HTML = """
<h2 style="margin-bottom:2px;">Pokémon Draft Searcher</h2>
<p style="color:#888; margin-top:0;">
    Developed by <b>Elliott Sneath</b>
    &nbsp;·&nbsp; GitHub: <b>elliottsneath</b>
    &nbsp;·&nbsp; Discord: <b>vapelordell</b>
</p>
<hr>

<h3>Settings</h3>
<p>
    The Settings page is where you configure your draft pool before searching.
</p>
<ul>
    <li><b>Select Pokémon</b> — tick/untick individual Pokémon from the full Pokédex list, then hit <b>Apply</b> to load your selection.</li>
    <li><b>Import from File</b> — load a <code>.pkmnlist</code> file shared by another player. This restores their exact selection and draft board.</li>
    <li><b>Import from Excel</b> — import directly from a draft board <code>.xlsx</code> file. The tool looks for a sheet named <b>Board</b> (or asks you to pick one). Pokémon listed under a <b>Banned</b> column header are automatically excluded.</li>
    <li><b>Import from Google Sheets</b> — paste your sheet URL and hit Sync. The sheet is downloaded and parsed the same way as Excel. Use <b>Sync</b> in the settings toolbar to refresh at any time.</li>
    <li><b>Export</b> — saves your current selection to a <code>.pkmnlist</code> file to share with other players.</li>
    <li><b>Reset</b> — marks every Pokémon as selected (full Pokédex).</li>
</ul>

<h3>Format</h3>
<p>
    The <b>Format</b> dropdown controls which moves are considered legal for each Pokémon.
    All move filtering, popup move lists, and team role analysis respect this setting.
</p>
<ul>
    <li><b>SV</b> — Generation 9 moves only.</li>
    <li><b>NatDex</b> — All moves from any generation.</li>
    <li><b>Champions</b> — Generation 9 moves plus Champions-specific additions.</li>
    <li><b>Champions NatDex</b> — All generations plus Champions-specific additions (default).</li>
</ul>
<p>Your selected format is saved automatically and restored on next launch.</p>

<h3>Pool</h3>
<p>
    If your draft has multiple pools, select your pool from the <b>Pool</b> dropdown.
    Pokémon drafted by another pool are still visible but marked as drafted.
    Set to <b>None</b> to see all drafted Pokémon regardless of pool.
</p>

<hr>

<h3>Main Page — Search &amp; Filter</h3>
<p>
    Type in the search bar and select a suggestion to add a filter chip.
    Multiple filters stack — a Pokémon must match <i>all</i> of them to appear.
    Click <b>×</b> on a chip to remove that filter, or <b>Clear</b> to remove all.
</p>
<ul>
    <li><b>Pokémon</b> — filter by name.</li>
    <li><b>Type</b> — filter by type (e.g. Water, Dragon).</li>
    <li><b>Ability</b> — filter by base or hidden ability.</li>
    <li><b>Move</b> — filter by move, using the currently selected format's movepools.</li>
</ul>
<p>
    Use the <b>stat headers</b> (HP, Atk, Def…) to sort the list. Click once to sort descending,
    again to sort ascending, a third time to clear.
    The <b>cost slider</b> filters by draft point cost when costs are loaded.
    <b>Hide Drafted</b> removes already-drafted Pokémon from the list.
</p>

<h3>Pokémon Popup</h3>
<p>
    Click any Pokémon in the list to open its popup. This shows base stats with colour-coded bars,
    type icons, and a move list filtered to the current format.
    Use the search box inside the popup to filter moves by name.
    Star a Pokémon to pin it to the top of the main list.
</p>

<hr>

<h3>Current Draft</h3>
<p>
    Add Pokémon to your team via the popup, and remove them by clicking their slot.
    Set your <b>Budget</b> and <b>Number of Picks</b> to enable the recommendation engine.
</p>
<ul>
    <li><b>Type coverage</b> — the top weaknesses, resistances, and immunities of your current team update live.</li>
    <li><b>Role recommendations</b> — the tool tracks missing team roles (Stealth Rock, Pivot, Trick Room, Cleric, etc.) and suggests the best available Pokémon to fill gaps, weighted by type coverage improvement and remaining budget.</li>
</ul>

<hr>

<h3>Debug Panel &nbsp;<kbd>F12</kbd></h3>
<p>
    Press <b>F12</b> at any time to toggle a dockable debug console at the bottom of the window.
    It captures all internal log output — data loads, cache hits, format changes, draft events,
    import results, and errors — useful for diagnosing unexpected behaviour.
    Press <b>F12</b> again or close the panel to hide it.
</p>
"""


class Ui_helpDialog:
    def setupUi(self, helpDialog):
        if not helpDialog.objectName():
            helpDialog.setObjectName("helpDialog")
        helpDialog.resize(520, 580)
        helpDialog.setWindowTitle("Help")

        layout = QVBoxLayout(helpDialog)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        browser = QTextBrowser(helpDialog)
        browser.setObjectName("helpBrowser")
        browser.setOpenExternalLinks(True)
        browser.setReadOnly(True)
        browser.setHtml(_HELP_HTML)
        layout.addWidget(browser)

        buttons = QDialogButtonBox(QDialogButtonBox.Close, helpDialog)
        buttons.rejected.connect(helpDialog.reject)
        layout.addWidget(buttons)

        QMetaObject.connectSlotsByName(helpDialog)

    def retranslateUi(self, helpDialog):
        pass
