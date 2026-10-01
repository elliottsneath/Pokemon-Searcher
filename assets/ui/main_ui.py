# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QSizePolicy,
    QSpacerItem, QStackedWidget, QStatusBar, QToolBar,
    QToolButton, QVBoxLayout, QWidget)

from assets.ui.animated_button import AnimatedHoverButton
from assets.ui.clickable_label import ClickableLabel
from common.custom_widgets import RangeSlider

class Ui_PokemonSearcher(object):
    def setupUi(self, PokemonSearcher):
        if not PokemonSearcher.objectName():
            PokemonSearcher.setObjectName(u"PokemonSearcher")
        PokemonSearcher.resize(756, 578)
        self.actionVersion = QAction(PokemonSearcher)
        self.actionVersion.setObjectName(u"actionVersion")
        self.actionVersion.setEnabled(False)
        self.actionSettings = QAction(PokemonSearcher)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionSettings.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.actionHelp = QAction(PokemonSearcher)
        self.actionHelp.setObjectName(u"actionHelp")
        self.actionHelp.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.actionCurrentDraft = QAction(PokemonSearcher)
        self.actionCurrentDraft.setObjectName(u"actionCurrentDraft")
        self.actionCurrentDraft.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.actionHome = QAction(PokemonSearcher)
        self.actionHome.setObjectName(u"actionHome")
        self.actionHome.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self.centralwidget = QWidget(PokemonSearcher)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.main = QWidget()
        self.main.setObjectName(u"main")
        self.verticalLayout_2 = QVBoxLayout(self.main)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.searchBar = QLineEdit(self.main)
        self.searchBar.setObjectName(u"searchBar")

        self.horizontalLayout_5.addWidget(self.searchBar)

        self.refreshButton = QToolButton(self.main)
        self.refreshButton.setObjectName(u"refreshButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        self.refreshButton.setIcon(icon)
        self.refreshButton.setAutoRaise(True)

        self.horizontalLayout_5.addWidget(self.refreshButton)

        self.clearFiltersButton = AnimatedHoverButton(self.main)
        self.clearFiltersButton.setObjectName(u"clearFiltersButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearFiltersButton.sizePolicy().hasHeightForWidth())
        self.clearFiltersButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.clearFiltersButton)

        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(2, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.filterLayout = QHBoxLayout()
        self.filterLayout.setObjectName(u"filterLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filterLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.filterLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.main)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_5)

        self.pokemonCheckbox = QCheckBox(self.main)
        self.pokemonCheckbox.setObjectName(u"pokemonCheckbox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pokemonCheckbox.sizePolicy().hasHeightForWidth())
        self.pokemonCheckbox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.pokemonCheckbox)

        self.typesCheckbox = QCheckBox(self.main)
        self.typesCheckbox.setObjectName(u"typesCheckbox")
        sizePolicy2.setHeightForWidth(self.typesCheckbox.sizePolicy().hasHeightForWidth())
        self.typesCheckbox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.typesCheckbox)

        self.abilitiesCheckbox = QCheckBox(self.main)
        self.abilitiesCheckbox.setObjectName(u"abilitiesCheckbox")
        sizePolicy2.setHeightForWidth(self.abilitiesCheckbox.sizePolicy().hasHeightForWidth())
        self.abilitiesCheckbox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.abilitiesCheckbox)

        self.movesCheckbox = QCheckBox(self.main)
        self.movesCheckbox.setObjectName(u"movesCheckbox")
        sizePolicy2.setHeightForWidth(self.movesCheckbox.sizePolicy().hasHeightForWidth())
        self.movesCheckbox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.movesCheckbox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_11 = QLabel(self.main)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_19.addWidget(self.label_11)

        self.horizontalSlider = RangeSlider(self.main)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_19.addWidget(self.horizontalSlider)

        self.hideDraftedCheckbox = QCheckBox(self.main)
        self.hideDraftedCheckbox.setObjectName(u"hideDraftedCheckbox")
        sizePolicy2.setHeightForWidth(self.hideDraftedCheckbox.sizePolicy().hasHeightForWidth())
        self.hideDraftedCheckbox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_19.addWidget(self.hideDraftedCheckbox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, 10, -1)
        self.nameLabel = ClickableLabel(self.main)
        self.nameLabel.setObjectName(u"nameLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.nameLabel.sizePolicy().hasHeightForWidth())
        self.nameLabel.setSizePolicy(sizePolicy3)
        self.nameLabel.setMinimumSize(QSize(120, 0))
        self.nameLabel.setBaseSize(QSize(0, 0))
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.nameLabel)

        self.costLabel = ClickableLabel(self.main)
        self.costLabel.setObjectName(u"costLabel")
        sizePolicy3.setHeightForWidth(self.costLabel.sizePolicy().hasHeightForWidth())
        self.costLabel.setSizePolicy(sizePolicy3)
        self.costLabel.setMinimumSize(QSize(30, 0))
        self.costLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.costLabel)

        self.typeLabel = QLabel(self.main)
        self.typeLabel.setObjectName(u"typeLabel")
        sizePolicy3.setHeightForWidth(self.typeLabel.sizePolicy().hasHeightForWidth())
        self.typeLabel.setSizePolicy(sizePolicy3)
        self.typeLabel.setMinimumSize(QSize(100, 0))
        self.typeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.typeLabel)

        self.ablilityLabel = QLabel(self.main)
        self.ablilityLabel.setObjectName(u"ablilityLabel")
        sizePolicy3.setHeightForWidth(self.ablilityLabel.sizePolicy().hasHeightForWidth())
        self.ablilityLabel.setSizePolicy(sizePolicy3)
        self.ablilityLabel.setMinimumSize(QSize(200, 0))
        self.ablilityLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.ablilityLabel)

        self.hpLabel = ClickableLabel(self.main)
        self.hpLabel.setObjectName(u"hpLabel")
        sizePolicy3.setHeightForWidth(self.hpLabel.sizePolicy().hasHeightForWidth())
        self.hpLabel.setSizePolicy(sizePolicy3)
        self.hpLabel.setMinimumSize(QSize(30, 0))
        self.hpLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.hpLabel)

        self.atkLabel = ClickableLabel(self.main)
        self.atkLabel.setObjectName(u"atkLabel")
        sizePolicy3.setHeightForWidth(self.atkLabel.sizePolicy().hasHeightForWidth())
        self.atkLabel.setSizePolicy(sizePolicy3)
        self.atkLabel.setMinimumSize(QSize(30, 0))
        self.atkLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.atkLabel)

        self.defLabel = ClickableLabel(self.main)
        self.defLabel.setObjectName(u"defLabel")
        sizePolicy3.setHeightForWidth(self.defLabel.sizePolicy().hasHeightForWidth())
        self.defLabel.setSizePolicy(sizePolicy3)
        self.defLabel.setMinimumSize(QSize(30, 0))
        self.defLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.defLabel)

        self.spaLabel = ClickableLabel(self.main)
        self.spaLabel.setObjectName(u"spaLabel")
        sizePolicy3.setHeightForWidth(self.spaLabel.sizePolicy().hasHeightForWidth())
        self.spaLabel.setSizePolicy(sizePolicy3)
        self.spaLabel.setMinimumSize(QSize(30, 0))
        self.spaLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.spaLabel)

        self.spdLabel = ClickableLabel(self.main)
        self.spdLabel.setObjectName(u"spdLabel")
        sizePolicy3.setHeightForWidth(self.spdLabel.sizePolicy().hasHeightForWidth())
        self.spdLabel.setSizePolicy(sizePolicy3)
        self.spdLabel.setMinimumSize(QSize(30, 0))
        self.spdLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.spdLabel)

        self.speLabel = ClickableLabel(self.main)
        self.speLabel.setObjectName(u"speLabel")
        sizePolicy3.setHeightForWidth(self.speLabel.sizePolicy().hasHeightForWidth())
        self.speLabel.setSizePolicy(sizePolicy3)
        self.speLabel.setMinimumSize(QSize(30, 0))
        self.speLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.speLabel)

        self.bstLabel = ClickableLabel(self.main)
        self.bstLabel.setObjectName(u"bstLabel")
        sizePolicy3.setHeightForWidth(self.bstLabel.sizePolicy().hasHeightForWidth())
        self.bstLabel.setSizePolicy(sizePolicy3)
        self.bstLabel.setMinimumSize(QSize(30, 0))
        self.bstLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.bstLabel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.pokemonListWidget = QListWidget(self.main)
        self.pokemonListWidget.setObjectName(u"pokemonListWidget")

        self.verticalLayout_2.addWidget(self.pokemonListWidget)

        self.stackedWidget.addWidget(self.main)
        self.settings = QWidget()
        self.settings.setObjectName(u"settings")
        self.verticalLayout_3 = QVBoxLayout(self.settings)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.budgetLineEdit = QLineEdit(self.settings)
        self.budgetLineEdit.setObjectName(u"budgetLineEdit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.budgetLineEdit.sizePolicy().hasHeightForWidth())
        self.budgetLineEdit.setSizePolicy(sizePolicy4)

        self.gridLayout_3.addWidget(self.budgetLineEdit, 0, 3, 1, 1)

        self.label_12 = QLabel(self.settings)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_3.addWidget(self.label_12, 0, 6, 1, 1)

        self.poolLabel = QLabel(self.settings)
        self.poolLabel.setObjectName(u"poolLabel")

        self.gridLayout_3.addWidget(self.poolLabel, 0, 0, 1, 1)

        self.poolComboBox = QComboBox(self.settings)
        self.poolComboBox.setObjectName(u"poolComboBox")

        self.gridLayout_3.addWidget(self.poolComboBox, 0, 1, 1, 1)

        self.label_4 = QLabel(self.settings)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 0, 4, 1, 1)

        self.noOfPokemonLineEdit = QLineEdit(self.settings)
        self.noOfPokemonLineEdit.setObjectName(u"noOfPokemonLineEdit")
        sizePolicy4.setHeightForWidth(self.noOfPokemonLineEdit.sizePolicy().hasHeightForWidth())
        self.noOfPokemonLineEdit.setSizePolicy(sizePolicy4)

        self.gridLayout_3.addWidget(self.noOfPokemonLineEdit, 0, 5, 1, 1)

        self.label_3 = QLabel(self.settings)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 2, 1, 1)

        self.formatCombo = QComboBox(self.settings)
        self.formatCombo.addItem("")
        self.formatCombo.addItem("")
        self.formatCombo.addItem("")
        self.formatCombo.addItem("")
        self.formatCombo.setObjectName(u"formatCombo")

        self.gridLayout_3.addWidget(self.formatCombo, 0, 7, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.applyButton = AnimatedHoverButton(self.settings)
        self.applyButton.setObjectName(u"applyButton")

        self.horizontalLayout_9.addWidget(self.applyButton)

        self.exportPokemonButton = AnimatedHoverButton(self.settings)
        self.exportPokemonButton.setObjectName(u"exportPokemonButton")

        self.horizontalLayout_9.addWidget(self.exportPokemonButton)

        self.importPokemonButton = AnimatedHoverButton(self.settings)
        self.importPokemonButton.setObjectName(u"importPokemonButton")

        self.horizontalLayout_9.addWidget(self.importPokemonButton)

        self.horizontalLayout_9.setStretch(0, 4)
        self.horizontalLayout_9.setStretch(1, 4)
        self.horizontalLayout_9.setStretch(2, 4)

        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.settings)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.settingsSearchBar = QLineEdit(self.settings)
        self.settingsSearchBar.setObjectName(u"settingsSearchBar")

        self.horizontalLayout.addWidget(self.settingsSearchBar)

        self.resetPokemonButton = AnimatedHoverButton(self.settings)
        self.resetPokemonButton.setObjectName(u"resetPokemonButton")

        self.horizontalLayout.addWidget(self.resetPokemonButton)

        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.settingsPokemonListWidget = QListWidget(self.settings)
        self.settingsPokemonListWidget.setObjectName(u"settingsPokemonListWidget")

        self.verticalLayout_3.addWidget(self.settingsPokemonListWidget)

        self.stackedWidget.addWidget(self.settings)
        self.currentDraft = QWidget()
        self.currentDraft.setObjectName(u"currentDraft")
        self.gridLayout = QGridLayout(self.currentDraft)
        self.gridLayout.setObjectName(u"gridLayout")
        self.dataFrame = QFrame(self.currentDraft)
        self.dataFrame.setObjectName(u"dataFrame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.dataFrame.sizePolicy().hasHeightForWidth())
        self.dataFrame.setSizePolicy(sizePolicy5)
        self.dataFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.horizontalLayout_4 = QHBoxLayout(self.dataFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.dataFrame)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.line = QFrame(self.dataFrame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line)

        self.picksLabel = QLabel(self.dataFrame)
        self.picksLabel.setObjectName(u"picksLabel")

        self.horizontalLayout_4.addWidget(self.picksLabel)

        self.line_2 = QFrame(self.dataFrame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_2)

        self.ptsLabel = QLabel(self.dataFrame)
        self.ptsLabel.setObjectName(u"ptsLabel")

        self.horizontalLayout_4.addWidget(self.ptsLabel)

        self.line_3 = QFrame(self.dataFrame)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_3)

        self.clearDraftButton = AnimatedHoverButton(self.dataFrame)
        self.clearDraftButton.setObjectName(u"clearDraftButton")

        self.horizontalLayout_4.addWidget(self.clearDraftButton)

        self.horizontalSpacer_3 = QSpacerItem(351, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.importLabel = QLabel(self.dataFrame)
        self.importLabel.setObjectName(u"importLabel")

        self.horizontalLayout_4.addWidget(self.importLabel)


        self.gridLayout.addWidget(self.dataFrame, 0, 0, 1, 2)

        self.typesFrame = QFrame(self.currentDraft)
        self.typesFrame.setObjectName(u"typesFrame")
        self.typesFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_4 = QVBoxLayout(self.typesFrame)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.label_6 = QLabel(self.typesFrame)
        self.label_6.setObjectName(u"label_6")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy6)

        self.verticalLayout_4.addWidget(self.label_6)

        self.widget_17 = QWidget(self.typesFrame)
        self.widget_17.setObjectName(u"widget_17")
        self.verticalLayout_6 = QVBoxLayout(self.widget_17)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(3, 3, 3, 3)
        self.label_8 = QLabel(self.widget_17)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_6.addWidget(self.label_8)

        self.weaknessesLayout = QHBoxLayout()
        self.weaknessesLayout.setObjectName(u"weaknessesLayout")

        self.verticalLayout_6.addLayout(self.weaknessesLayout)


        self.verticalLayout_4.addWidget(self.widget_17)

        self.widget_18 = QWidget(self.typesFrame)
        self.widget_18.setObjectName(u"widget_18")
        self.verticalLayout_7 = QVBoxLayout(self.widget_18)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(3, 3, 3, 3)
        self.label_9 = QLabel(self.widget_18)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_7.addWidget(self.label_9)

        self.resistancesLayout = QHBoxLayout()
        self.resistancesLayout.setObjectName(u"resistancesLayout")

        self.verticalLayout_7.addLayout(self.resistancesLayout)


        self.verticalLayout_4.addWidget(self.widget_18)

        self.widget_19 = QWidget(self.typesFrame)
        self.widget_19.setObjectName(u"widget_19")
        self.verticalLayout_8 = QVBoxLayout(self.widget_19)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(3, 3, 3, 3)
        self.label_10 = QLabel(self.widget_19)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_8.addWidget(self.label_10)

        self.immunitiesLayout = QHBoxLayout()
        self.immunitiesLayout.setObjectName(u"immunitiesLayout")

        self.verticalLayout_8.addLayout(self.immunitiesLayout)


        self.verticalLayout_4.addWidget(self.widget_19)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.typesFrame, 2, 0, 1, 1)

        self.recommendationsFrame = QFrame(self.currentDraft)
        self.recommendationsFrame.setObjectName(u"recommendationsFrame")
        sizePolicy1.setHeightForWidth(self.recommendationsFrame.sizePolicy().hasHeightForWidth())
        self.recommendationsFrame.setSizePolicy(sizePolicy1)
        self.recommendationsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_5 = QVBoxLayout(self.recommendationsFrame)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.label_7 = QLabel(self.recommendationsFrame)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_5.addWidget(self.label_7)

        self.widget = QWidget(self.recommendationsFrame)
        self.widget.setObjectName(u"widget")
        self.gridLayout_4 = QGridLayout(self.widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(3, 3, 3, 3)
        self.recTypeLayout = QHBoxLayout()
        self.recTypeLayout.setObjectName(u"recTypeLayout")

        self.gridLayout_4.addLayout(self.recTypeLayout, 1, 1, 1, 1)

        self.recReason_1 = QLabel(self.widget)
        self.recReason_1.setObjectName(u"recReason_1")

        self.gridLayout_4.addWidget(self.recReason_1, 2, 1, 1, 2)

        self.recSprite_1 = QLabel(self.widget)
        self.recSprite_1.setObjectName(u"recSprite_1")

        self.gridLayout_4.addWidget(self.recSprite_1, 0, 0, 3, 1)

        self.recName_1 = QLabel(self.widget)
        self.recName_1.setObjectName(u"recName_1")

        self.gridLayout_4.addWidget(self.recName_1, 0, 1, 1, 1)

        self.recPts_1 = QLabel(self.widget)
        self.recPts_1.setObjectName(u"recPts_1")

        self.gridLayout_4.addWidget(self.recPts_1, 1, 2, 1, 1)

        self.recAdd_1 = QToolButton(self.widget)
        self.recAdd_1.setObjectName(u"recAdd_1")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.recAdd_1.setIcon(icon1)
        self.recAdd_1.setAutoRaise(True)

        self.gridLayout_4.addWidget(self.recAdd_1, 0, 3, 3, 1)


        self.verticalLayout_5.addWidget(self.widget)

        self.widget_2 = QWidget(self.recommendationsFrame)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_5 = QGridLayout(self.widget_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(3, 3, 3, 3)
        self.recTypeLayout_2 = QHBoxLayout()
        self.recTypeLayout_2.setObjectName(u"recTypeLayout_2")

        self.gridLayout_5.addLayout(self.recTypeLayout_2, 1, 1, 1, 1)

        self.recReason_2 = QLabel(self.widget_2)
        self.recReason_2.setObjectName(u"recReason_2")

        self.gridLayout_5.addWidget(self.recReason_2, 2, 1, 1, 2)

        self.recSprite_2 = QLabel(self.widget_2)
        self.recSprite_2.setObjectName(u"recSprite_2")

        self.gridLayout_5.addWidget(self.recSprite_2, 0, 0, 3, 1)

        self.recName_2 = QLabel(self.widget_2)
        self.recName_2.setObjectName(u"recName_2")

        self.gridLayout_5.addWidget(self.recName_2, 0, 1, 1, 1)

        self.recPts_2 = QLabel(self.widget_2)
        self.recPts_2.setObjectName(u"recPts_2")

        self.gridLayout_5.addWidget(self.recPts_2, 1, 2, 1, 1)

        self.recAdd_2 = QToolButton(self.widget_2)
        self.recAdd_2.setObjectName(u"recAdd_2")
        self.recAdd_2.setIcon(icon1)
        self.recAdd_2.setAutoRaise(True)

        self.gridLayout_5.addWidget(self.recAdd_2, 0, 3, 3, 1)


        self.verticalLayout_5.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.recommendationsFrame)
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout_6 = QGridLayout(self.widget_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(3, 3, 3, 3)
        self.recTypeLayout_3 = QHBoxLayout()
        self.recTypeLayout_3.setObjectName(u"recTypeLayout_3")

        self.gridLayout_6.addLayout(self.recTypeLayout_3, 1, 1, 1, 1)

        self.recReason_3 = QLabel(self.widget_3)
        self.recReason_3.setObjectName(u"recReason_3")

        self.gridLayout_6.addWidget(self.recReason_3, 2, 1, 1, 2)

        self.recSprite_3 = QLabel(self.widget_3)
        self.recSprite_3.setObjectName(u"recSprite_3")

        self.gridLayout_6.addWidget(self.recSprite_3, 0, 0, 3, 1)

        self.recName_3 = QLabel(self.widget_3)
        self.recName_3.setObjectName(u"recName_3")

        self.gridLayout_6.addWidget(self.recName_3, 0, 1, 1, 1)

        self.recPts_3 = QLabel(self.widget_3)
        self.recPts_3.setObjectName(u"recPts_3")

        self.gridLayout_6.addWidget(self.recPts_3, 1, 2, 1, 1)

        self.recAdd_3 = QToolButton(self.widget_3)
        self.recAdd_3.setObjectName(u"recAdd_3")
        self.recAdd_3.setIcon(icon1)
        self.recAdd_3.setAutoRaise(True)

        self.gridLayout_6.addWidget(self.recAdd_3, 0, 3, 3, 1)


        self.verticalLayout_5.addWidget(self.widget_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.gridLayout.addWidget(self.recommendationsFrame, 2, 1, 1, 1)

        self.draftedFrame = QFrame(self.currentDraft)
        self.draftedFrame.setObjectName(u"draftedFrame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.draftedFrame.sizePolicy().hasHeightForWidth())
        self.draftedFrame.setSizePolicy(sizePolicy7)
        self.draftedFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_2 = QGridLayout(self.draftedFrame)
        self.gridLayout_2.setSpacing(3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.pick_01_widget = QWidget(self.draftedFrame)
        self.pick_01_widget.setObjectName(u"pick_01_widget")
        self.verticalLayout_20 = QVBoxLayout(self.pick_01_widget)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.pick_01_sprite = QLabel(self.pick_01_widget)
        self.pick_01_sprite.setObjectName(u"pick_01_sprite")

        self.verticalLayout_20.addWidget(self.pick_01_sprite)

        self.pick_01_name = QLabel(self.pick_01_widget)
        self.pick_01_name.setObjectName(u"pick_01_name")

        self.verticalLayout_20.addWidget(self.pick_01_name)

        self.pick_01_type = QWidget(self.pick_01_widget)
        self.pick_01_type.setObjectName(u"pick_01_type")
        self.horizontalLayout_6 = QHBoxLayout(self.pick_01_type)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_20.addWidget(self.pick_01_type)

        self.pick_01_pts = QLabel(self.pick_01_widget)
        self.pick_01_pts.setObjectName(u"pick_01_pts")

        self.verticalLayout_20.addWidget(self.pick_01_pts)


        self.gridLayout_2.addWidget(self.pick_01_widget, 0, 0, 1, 1)

        self.pick_02_widget = QWidget(self.draftedFrame)
        self.pick_02_widget.setObjectName(u"pick_02_widget")
        self.verticalLayout_19 = QVBoxLayout(self.pick_02_widget)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.pick_02_sprite = QLabel(self.pick_02_widget)
        self.pick_02_sprite.setObjectName(u"pick_02_sprite")

        self.verticalLayout_19.addWidget(self.pick_02_sprite)

        self.pick_02_name = QLabel(self.pick_02_widget)
        self.pick_02_name.setObjectName(u"pick_02_name")

        self.verticalLayout_19.addWidget(self.pick_02_name)

        self.pick_02_type = QWidget(self.pick_02_widget)
        self.pick_02_type.setObjectName(u"pick_02_type")
        self.horizontalLayout_7 = QHBoxLayout(self.pick_02_type)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_19.addWidget(self.pick_02_type)

        self.pick_02_pts = QLabel(self.pick_02_widget)
        self.pick_02_pts.setObjectName(u"pick_02_pts")

        self.verticalLayout_19.addWidget(self.pick_02_pts)


        self.gridLayout_2.addWidget(self.pick_02_widget, 0, 1, 1, 1)

        self.pick_03_widget = QWidget(self.draftedFrame)
        self.pick_03_widget.setObjectName(u"pick_03_widget")
        self.verticalLayout_18 = QVBoxLayout(self.pick_03_widget)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.pick_03_sprite = QLabel(self.pick_03_widget)
        self.pick_03_sprite.setObjectName(u"pick_03_sprite")

        self.verticalLayout_18.addWidget(self.pick_03_sprite)

        self.pick_03_name = QLabel(self.pick_03_widget)
        self.pick_03_name.setObjectName(u"pick_03_name")

        self.verticalLayout_18.addWidget(self.pick_03_name)

        self.pick_03_type = QWidget(self.pick_03_widget)
        self.pick_03_type.setObjectName(u"pick_03_type")
        self.horizontalLayout_8 = QHBoxLayout(self.pick_03_type)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_18.addWidget(self.pick_03_type)

        self.pick_03_pts = QLabel(self.pick_03_widget)
        self.pick_03_pts.setObjectName(u"pick_03_pts")

        self.verticalLayout_18.addWidget(self.pick_03_pts)


        self.gridLayout_2.addWidget(self.pick_03_widget, 0, 2, 1, 1)

        self.pick_04_widget = QWidget(self.draftedFrame)
        self.pick_04_widget.setObjectName(u"pick_04_widget")
        self.verticalLayout_17 = QVBoxLayout(self.pick_04_widget)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.pick_04_sprite = QLabel(self.pick_04_widget)
        self.pick_04_sprite.setObjectName(u"pick_04_sprite")

        self.verticalLayout_17.addWidget(self.pick_04_sprite)

        self.pick_04_name = QLabel(self.pick_04_widget)
        self.pick_04_name.setObjectName(u"pick_04_name")

        self.verticalLayout_17.addWidget(self.pick_04_name)

        self.pick_04_type = QWidget(self.pick_04_widget)
        self.pick_04_type.setObjectName(u"pick_04_type")
        self.horizontalLayout_10 = QHBoxLayout(self.pick_04_type)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_17.addWidget(self.pick_04_type)

        self.pick_04_pts = QLabel(self.pick_04_widget)
        self.pick_04_pts.setObjectName(u"pick_04_pts")

        self.verticalLayout_17.addWidget(self.pick_04_pts)


        self.gridLayout_2.addWidget(self.pick_04_widget, 0, 3, 1, 1)

        self.pick_05_widget = QWidget(self.draftedFrame)
        self.pick_05_widget.setObjectName(u"pick_05_widget")
        self.verticalLayout_16 = QVBoxLayout(self.pick_05_widget)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.pick_05_sprite = QLabel(self.pick_05_widget)
        self.pick_05_sprite.setObjectName(u"pick_05_sprite")

        self.verticalLayout_16.addWidget(self.pick_05_sprite)

        self.pick_05_name = QLabel(self.pick_05_widget)
        self.pick_05_name.setObjectName(u"pick_05_name")

        self.verticalLayout_16.addWidget(self.pick_05_name)

        self.pick_05_type = QWidget(self.pick_05_widget)
        self.pick_05_type.setObjectName(u"pick_05_type")
        self.horizontalLayout_11 = QHBoxLayout(self.pick_05_type)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_16.addWidget(self.pick_05_type)

        self.pick_05_pts = QLabel(self.pick_05_widget)
        self.pick_05_pts.setObjectName(u"pick_05_pts")

        self.verticalLayout_16.addWidget(self.pick_05_pts)


        self.gridLayout_2.addWidget(self.pick_05_widget, 0, 4, 1, 1)

        self.pick_06_widget = QWidget(self.draftedFrame)
        self.pick_06_widget.setObjectName(u"pick_06_widget")
        self.verticalLayout_15 = QVBoxLayout(self.pick_06_widget)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.pick_06_sprite = QLabel(self.pick_06_widget)
        self.pick_06_sprite.setObjectName(u"pick_06_sprite")

        self.verticalLayout_15.addWidget(self.pick_06_sprite)

        self.pick_06_name = QLabel(self.pick_06_widget)
        self.pick_06_name.setObjectName(u"pick_06_name")

        self.verticalLayout_15.addWidget(self.pick_06_name)

        self.pick_06_type = QWidget(self.pick_06_widget)
        self.pick_06_type.setObjectName(u"pick_06_type")
        self.horizontalLayout_12 = QHBoxLayout(self.pick_06_type)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_15.addWidget(self.pick_06_type)

        self.pick_06_pts = QLabel(self.pick_06_widget)
        self.pick_06_pts.setObjectName(u"pick_06_pts")

        self.verticalLayout_15.addWidget(self.pick_06_pts)


        self.gridLayout_2.addWidget(self.pick_06_widget, 0, 5, 1, 1)

        self.pick_07_widget = QWidget(self.draftedFrame)
        self.pick_07_widget.setObjectName(u"pick_07_widget")
        self.verticalLayout_14 = QVBoxLayout(self.pick_07_widget)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.pick_07_sprite = QLabel(self.pick_07_widget)
        self.pick_07_sprite.setObjectName(u"pick_07_sprite")

        self.verticalLayout_14.addWidget(self.pick_07_sprite)

        self.pick_07_name = QLabel(self.pick_07_widget)
        self.pick_07_name.setObjectName(u"pick_07_name")

        self.verticalLayout_14.addWidget(self.pick_07_name)

        self.pick_07_type = QWidget(self.pick_07_widget)
        self.pick_07_type.setObjectName(u"pick_07_type")
        self.horizontalLayout_13 = QHBoxLayout(self.pick_07_type)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_14.addWidget(self.pick_07_type)

        self.pick_07_pts = QLabel(self.pick_07_widget)
        self.pick_07_pts.setObjectName(u"pick_07_pts")

        self.verticalLayout_14.addWidget(self.pick_07_pts)


        self.gridLayout_2.addWidget(self.pick_07_widget, 1, 0, 1, 1)

        self.pick_08_widget = QWidget(self.draftedFrame)
        self.pick_08_widget.setObjectName(u"pick_08_widget")
        self.verticalLayout_13 = QVBoxLayout(self.pick_08_widget)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.pick_08_sprite = QLabel(self.pick_08_widget)
        self.pick_08_sprite.setObjectName(u"pick_08_sprite")

        self.verticalLayout_13.addWidget(self.pick_08_sprite)

        self.pick_08_name = QLabel(self.pick_08_widget)
        self.pick_08_name.setObjectName(u"pick_08_name")

        self.verticalLayout_13.addWidget(self.pick_08_name)

        self.pick_08_type = QWidget(self.pick_08_widget)
        self.pick_08_type.setObjectName(u"pick_08_type")
        self.horizontalLayout_14 = QHBoxLayout(self.pick_08_type)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_13.addWidget(self.pick_08_type)

        self.pick_08_pts = QLabel(self.pick_08_widget)
        self.pick_08_pts.setObjectName(u"pick_08_pts")

        self.verticalLayout_13.addWidget(self.pick_08_pts)


        self.gridLayout_2.addWidget(self.pick_08_widget, 1, 1, 1, 1)

        self.pick_09_widget = QWidget(self.draftedFrame)
        self.pick_09_widget.setObjectName(u"pick_09_widget")
        self.verticalLayout_12 = QVBoxLayout(self.pick_09_widget)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.pick_09_sprite = QLabel(self.pick_09_widget)
        self.pick_09_sprite.setObjectName(u"pick_09_sprite")

        self.verticalLayout_12.addWidget(self.pick_09_sprite)

        self.pick_09_name = QLabel(self.pick_09_widget)
        self.pick_09_name.setObjectName(u"pick_09_name")

        self.verticalLayout_12.addWidget(self.pick_09_name)

        self.pick_09_type = QWidget(self.pick_09_widget)
        self.pick_09_type.setObjectName(u"pick_09_type")
        self.horizontalLayout_15 = QHBoxLayout(self.pick_09_type)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_12.addWidget(self.pick_09_type)

        self.pick_09_pts = QLabel(self.pick_09_widget)
        self.pick_09_pts.setObjectName(u"pick_09_pts")

        self.verticalLayout_12.addWidget(self.pick_09_pts)


        self.gridLayout_2.addWidget(self.pick_09_widget, 1, 2, 1, 1)

        self.pick_10_widget = QWidget(self.draftedFrame)
        self.pick_10_widget.setObjectName(u"pick_10_widget")
        self.verticalLayout_11 = QVBoxLayout(self.pick_10_widget)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.pick_10_sprite = QLabel(self.pick_10_widget)
        self.pick_10_sprite.setObjectName(u"pick_10_sprite")

        self.verticalLayout_11.addWidget(self.pick_10_sprite)

        self.pick_10_name = QLabel(self.pick_10_widget)
        self.pick_10_name.setObjectName(u"pick_10_name")

        self.verticalLayout_11.addWidget(self.pick_10_name)

        self.pick_10_type = QWidget(self.pick_10_widget)
        self.pick_10_type.setObjectName(u"pick_10_type")
        self.horizontalLayout_16 = QHBoxLayout(self.pick_10_type)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_11.addWidget(self.pick_10_type)

        self.pick_10_pts = QLabel(self.pick_10_widget)
        self.pick_10_pts.setObjectName(u"pick_10_pts")

        self.verticalLayout_11.addWidget(self.pick_10_pts)


        self.gridLayout_2.addWidget(self.pick_10_widget, 1, 3, 1, 1)

        self.pick_11_widget = QWidget(self.draftedFrame)
        self.pick_11_widget.setObjectName(u"pick_11_widget")
        self.verticalLayout_10 = QVBoxLayout(self.pick_11_widget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.pick_11_sprite = QLabel(self.pick_11_widget)
        self.pick_11_sprite.setObjectName(u"pick_11_sprite")

        self.verticalLayout_10.addWidget(self.pick_11_sprite)

        self.pick_11_name = QLabel(self.pick_11_widget)
        self.pick_11_name.setObjectName(u"pick_11_name")

        self.verticalLayout_10.addWidget(self.pick_11_name)

        self.pick_11_type = QWidget(self.pick_11_widget)
        self.pick_11_type.setObjectName(u"pick_11_type")
        self.horizontalLayout_17 = QHBoxLayout(self.pick_11_type)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_10.addWidget(self.pick_11_type)

        self.pick_11_pts = QLabel(self.pick_11_widget)
        self.pick_11_pts.setObjectName(u"pick_11_pts")

        self.verticalLayout_10.addWidget(self.pick_11_pts)


        self.gridLayout_2.addWidget(self.pick_11_widget, 1, 4, 1, 1)

        self.pick_12_widget = QWidget(self.draftedFrame)
        self.pick_12_widget.setObjectName(u"pick_12_widget")
        self.verticalLayout_9 = QVBoxLayout(self.pick_12_widget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.pick_12_sprite = QLabel(self.pick_12_widget)
        self.pick_12_sprite.setObjectName(u"pick_12_sprite")

        self.verticalLayout_9.addWidget(self.pick_12_sprite)

        self.pick_12_name = QLabel(self.pick_12_widget)
        self.pick_12_name.setObjectName(u"pick_12_name")

        self.verticalLayout_9.addWidget(self.pick_12_name)

        self.pick_12_type = QWidget(self.pick_12_widget)
        self.pick_12_type.setObjectName(u"pick_12_type")
        self.horizontalLayout_18 = QHBoxLayout(self.pick_12_type)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_9.addWidget(self.pick_12_type)

        self.pick_12_pts = QLabel(self.pick_12_widget)
        self.pick_12_pts.setObjectName(u"pick_12_pts")

        self.verticalLayout_9.addWidget(self.pick_12_pts)


        self.gridLayout_2.addWidget(self.pick_12_widget, 1, 5, 1, 1)


        self.gridLayout.addWidget(self.draftedFrame, 1, 0, 1, 2)

        self.stackedWidget.addWidget(self.currentDraft)

        self.verticalLayout.addWidget(self.stackedWidget)

        PokemonSearcher.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(PokemonSearcher)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        PokemonSearcher.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.versionStatusBar = QStatusBar(PokemonSearcher)
        self.versionStatusBar.setObjectName(u"versionStatusBar")
        PokemonSearcher.setStatusBar(self.versionStatusBar)

        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionVersion)
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionCurrentDraft)
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionHelp)

        self.retranslateUi(PokemonSearcher)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PokemonSearcher)
    # setupUi

    def retranslateUi(self, PokemonSearcher):
        PokemonSearcher.setWindowTitle(QCoreApplication.translate("PokemonSearcher", u"MainWindow", None))
        self.actionVersion.setText(QCoreApplication.translate("PokemonSearcher", u"Version 1.0", None))
        self.actionSettings.setText(QCoreApplication.translate("PokemonSearcher", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.actionSettings.setToolTip(QCoreApplication.translate("PokemonSearcher", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.actionHelp.setText(QCoreApplication.translate("PokemonSearcher", u"Help", None))
        self.actionCurrentDraft.setText(QCoreApplication.translate("PokemonSearcher", u"Current Draft", None))
        self.actionHome.setText(QCoreApplication.translate("PokemonSearcher", u"Home", None))
        self.searchBar.setPlaceholderText(QCoreApplication.translate("PokemonSearcher", u"Search Pokemon, Move, Type, Ability, etc...", None))
        self.refreshButton.setText(QCoreApplication.translate("PokemonSearcher", u"...", None))
        self.clearFiltersButton.setText(QCoreApplication.translate("PokemonSearcher", u"Clear Filters", None))
        self.label_5.setText(QCoreApplication.translate("PokemonSearcher", u"Leave all blank to search for all:", None))
        self.pokemonCheckbox.setText(QCoreApplication.translate("PokemonSearcher", u"Pokemon", None))
        self.typesCheckbox.setText(QCoreApplication.translate("PokemonSearcher", u"Types", None))
        self.abilitiesCheckbox.setText(QCoreApplication.translate("PokemonSearcher", u"Abilities", None))
        self.movesCheckbox.setText(QCoreApplication.translate("PokemonSearcher", u"Moves", None))
        self.label_11.setText(QCoreApplication.translate("PokemonSearcher", u"Price Range: ", None))
        self.hideDraftedCheckbox.setText(QCoreApplication.translate("PokemonSearcher", u"Hide drafted", None))
        self.nameLabel.setText(QCoreApplication.translate("PokemonSearcher", u"Name", None))
        self.costLabel.setText(QCoreApplication.translate("PokemonSearcher", u"Pts", None))
        self.typeLabel.setText(QCoreApplication.translate("PokemonSearcher", u"Types", None))
        self.ablilityLabel.setText(QCoreApplication.translate("PokemonSearcher", u"Abilities", None))
        self.hpLabel.setText(QCoreApplication.translate("PokemonSearcher", u"HP", None))
        self.atkLabel.setText(QCoreApplication.translate("PokemonSearcher", u"Atk", None))
        self.defLabel.setText(QCoreApplication.translate("PokemonSearcher", u"Def", None))
        self.spaLabel.setText(QCoreApplication.translate("PokemonSearcher", u"SpA", None))
        self.spdLabel.setText(QCoreApplication.translate("PokemonSearcher", u"SpD", None))
        self.speLabel.setText(QCoreApplication.translate("PokemonSearcher", u"Spe", None))
        self.bstLabel.setText(QCoreApplication.translate("PokemonSearcher", u"BST", None))
        self.label_12.setText(QCoreApplication.translate("PokemonSearcher", u"Format: ", None))
        self.poolLabel.setText(QCoreApplication.translate("PokemonSearcher", u"Draft pool:", None))
        self.label_4.setText(QCoreApplication.translate("PokemonSearcher", u"No. of Pokemon", None))
        self.label_3.setText(QCoreApplication.translate("PokemonSearcher", u"Budget:", None))
        self.formatCombo.setItemText(0, QCoreApplication.translate("PokemonSearcher", u"SV", None))
        self.formatCombo.setItemText(1, QCoreApplication.translate("PokemonSearcher", u"NatDex", None))
        self.formatCombo.setItemText(2, QCoreApplication.translate("PokemonSearcher", u"Champions", None))
        self.formatCombo.setItemText(3, QCoreApplication.translate("PokemonSearcher", u"Champions NatDex", None))

        self.applyButton.setText(QCoreApplication.translate("PokemonSearcher", u"Apply", None))
        self.exportPokemonButton.setText(QCoreApplication.translate("PokemonSearcher", u"Export Pokemon List", None))
        self.importPokemonButton.setText(QCoreApplication.translate("PokemonSearcher", u"Import Pokemon List", None))
        self.label_2.setText(QCoreApplication.translate("PokemonSearcher", u"Enabled Pokemon:", None))
        self.settingsSearchBar.setPlaceholderText(QCoreApplication.translate("PokemonSearcher", u"Search Pokemon...", None))
        self.resetPokemonButton.setText(QCoreApplication.translate("PokemonSearcher", u"Reset Pokemon List", None))
        self.label.setText(QCoreApplication.translate("PokemonSearcher", u"Current Draft", None))
        self.picksLabel.setText(QCoreApplication.translate("PokemonSearcher", u"x/12 Picks", None))
        self.ptsLabel.setText(QCoreApplication.translate("PokemonSearcher", u"x Pts Remaining", None))
        self.clearDraftButton.setText(QCoreApplication.translate("PokemonSearcher", u"Clear", None))
        self.importLabel.setText(QCoreApplication.translate("PokemonSearcher", u"Import Refreshed x ago", None))
        self.label_6.setText(QCoreApplication.translate("PokemonSearcher", u"Type Matchups", None))
        self.label_8.setText(QCoreApplication.translate("PokemonSearcher", u"Main Weaknesses", None))
        self.label_9.setText(QCoreApplication.translate("PokemonSearcher", u"Key Resistances", None))
        self.label_10.setText(QCoreApplication.translate("PokemonSearcher", u"Immunities", None))
        self.label_7.setText(QCoreApplication.translate("PokemonSearcher", u"Recommendations", None))
        self.recReason_1.setText("")
        self.recSprite_1.setText("")
        self.recName_1.setText("")
        self.recPts_1.setText("")
        self.recAdd_1.setText(QCoreApplication.translate("PokemonSearcher", u"...", None))
        self.recReason_2.setText("")
        self.recSprite_2.setText("")
        self.recName_2.setText("")
        self.recPts_2.setText("")
        self.recAdd_2.setText(QCoreApplication.translate("PokemonSearcher", u"...", None))
        self.recReason_3.setText("")
        self.recSprite_3.setText("")
        self.recName_3.setText("")
        self.recPts_3.setText("")
        self.recAdd_3.setText(QCoreApplication.translate("PokemonSearcher", u"...", None))
        self.pick_01_sprite.setText("")
        self.pick_01_name.setText("")
        self.pick_01_pts.setText("")
        self.pick_02_sprite.setText("")
        self.pick_02_name.setText("")
        self.pick_02_pts.setText("")
        self.pick_03_sprite.setText("")
        self.pick_03_name.setText("")
        self.pick_03_pts.setText("")
        self.pick_04_sprite.setText("")
        self.pick_04_name.setText("")
        self.pick_04_pts.setText("")
        self.pick_05_sprite.setText("")
        self.pick_05_name.setText("")
        self.pick_05_pts.setText("")
        self.pick_06_sprite.setText("")
        self.pick_06_name.setText("")
        self.pick_06_pts.setText("")
        self.pick_07_sprite.setText("")
        self.pick_07_name.setText("")
        self.pick_07_pts.setText("")
        self.pick_08_sprite.setText("")
        self.pick_08_name.setText("")
        self.pick_08_pts.setText("")
        self.pick_09_sprite.setText("")
        self.pick_09_name.setText("")
        self.pick_09_pts.setText("")
        self.pick_10_sprite.setText("")
        self.pick_10_name.setText("")
        self.pick_10_pts.setText("")
        self.pick_11_sprite.setText("")
        self.pick_11_name.setText("")
        self.pick_11_pts.setText("")
        self.pick_12_sprite.setText("")
        self.pick_12_name.setText("")
        self.pick_12_pts.setText("")
        self.toolBar.setWindowTitle(QCoreApplication.translate("PokemonSearcher", u"toolBar", None))
    # retranslateUi

