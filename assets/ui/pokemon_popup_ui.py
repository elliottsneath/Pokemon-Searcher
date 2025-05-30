# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pokemon_popup.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from assets.ui.clickable_label import ClickableLabel
from assets.ui.stats_bar_widget import StatBar

class Ui_PokemonPopup(object):
    def setupUi(self, PokemonPopup):
        if not PokemonPopup.objectName():
            PokemonPopup.setObjectName(u"PokemonPopup")
        PokemonPopup.resize(400, 338)
        self.verticalLayout = QVBoxLayout(PokemonPopup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.nameLabel = QLabel(PokemonPopup)
        self.nameLabel.setObjectName(u"nameLabel")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.nameLabel.setFont(font)

        self.horizontalLayout_2.addWidget(self.nameLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.starLabel = ClickableLabel(PokemonPopup)
        self.starLabel.setObjectName(u"starLabel")

        self.horizontalLayout_2.addWidget(self.starLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.type1Label = QLabel(PokemonPopup)
        self.type1Label.setObjectName(u"type1Label")

        self.horizontalLayout.addWidget(self.type1Label)

        self.type2Label = QLabel(PokemonPopup)
        self.type2Label.setObjectName(u"type2Label")

        self.horizontalLayout.addWidget(self.type2Label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QFrame(PokemonPopup)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_5 = QLabel(PokemonPopup)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_2 = QLabel(PokemonPopup)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.spdStatBar = StatBar(PokemonPopup)
        self.spdStatBar.setObjectName(u"spdStatBar")

        self.gridLayout.addWidget(self.spdStatBar, 4, 2, 1, 1)

        self.spaStatBar = StatBar(PokemonPopup)
        self.spaStatBar.setObjectName(u"spaStatBar")

        self.gridLayout.addWidget(self.spaStatBar, 3, 2, 1, 1)

        self.defStatBar = StatBar(PokemonPopup)
        self.defStatBar.setObjectName(u"defStatBar")

        self.gridLayout.addWidget(self.defStatBar, 2, 2, 1, 1)

        self.label_7 = QLabel(PokemonPopup)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)

        self.label_3 = QLabel(PokemonPopup)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_4 = QLabel(PokemonPopup)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.hpStatBar = StatBar(PokemonPopup)
        self.hpStatBar.setObjectName(u"hpStatBar")

        self.gridLayout.addWidget(self.hpStatBar, 0, 2, 1, 1)

        self.speStatBar = StatBar(PokemonPopup)
        self.speStatBar.setObjectName(u"speStatBar")

        self.gridLayout.addWidget(self.speStatBar, 5, 2, 1, 1)

        self.label_6 = QLabel(PokemonPopup)
        self.label_6.setObjectName(u"label_6")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.atkStatBar = StatBar(PokemonPopup)
        self.atkStatBar.setObjectName(u"atkStatBar")

        self.gridLayout.addWidget(self.atkStatBar, 1, 2, 1, 1)

        self.hpNumLabel = QLabel(PokemonPopup)
        self.hpNumLabel.setObjectName(u"hpNumLabel")

        self.gridLayout.addWidget(self.hpNumLabel, 0, 1, 1, 1)

        self.atkNumLabel = QLabel(PokemonPopup)
        self.atkNumLabel.setObjectName(u"atkNumLabel")

        self.gridLayout.addWidget(self.atkNumLabel, 1, 1, 1, 1)

        self.defNumLabel = QLabel(PokemonPopup)
        self.defNumLabel.setObjectName(u"defNumLabel")

        self.gridLayout.addWidget(self.defNumLabel, 2, 1, 1, 1)

        self.spaNumLabel = QLabel(PokemonPopup)
        self.spaNumLabel.setObjectName(u"spaNumLabel")

        self.gridLayout.addWidget(self.spaNumLabel, 3, 1, 1, 1)

        self.spdNumLabel = QLabel(PokemonPopup)
        self.spdNumLabel.setObjectName(u"spdNumLabel")
        sizePolicy.setHeightForWidth(self.spdNumLabel.sizePolicy().hasHeightForWidth())
        self.spdNumLabel.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.spdNumLabel, 4, 1, 1, 1)

        self.speNumLabel = QLabel(PokemonPopup)
        self.speNumLabel.setObjectName(u"speNumLabel")

        self.gridLayout.addWidget(self.speNumLabel, 5, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.line_2 = QFrame(PokemonPopup)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label = QLabel(PokemonPopup)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(PokemonPopup)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)

        self.moveListWidget = QListWidget(PokemonPopup)
        self.moveListWidget.setObjectName(u"moveListWidget")

        self.verticalLayout.addWidget(self.moveListWidget)


        self.retranslateUi(PokemonPopup)

        QMetaObject.connectSlotsByName(PokemonPopup)
    # setupUi

    def retranslateUi(self, PokemonPopup):
        PokemonPopup.setWindowTitle(QCoreApplication.translate("PokemonPopup", u"Dialog", None))
        self.nameLabel.setText(QCoreApplication.translate("PokemonPopup", u"TextLabel", None))
        self.starLabel.setText(QCoreApplication.translate("PokemonPopup", u"star", None))
        self.type1Label.setText(QCoreApplication.translate("PokemonPopup", u"TextLabel", None))
        self.type2Label.setText(QCoreApplication.translate("PokemonPopup", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("PokemonPopup", u"Special Attack", None))
        self.label_2.setText(QCoreApplication.translate("PokemonPopup", u"HP", None))
        self.label_7.setText(QCoreApplication.translate("PokemonPopup", u"Speed", None))
        self.label_3.setText(QCoreApplication.translate("PokemonPopup", u"Attack", None))
        self.label_4.setText(QCoreApplication.translate("PokemonPopup", u"Defense", None))
        self.label_6.setText(QCoreApplication.translate("PokemonPopup", u"Special Defense             ", None))
        self.hpNumLabel.setText(QCoreApplication.translate("PokemonPopup", u"hp", None))
        self.atkNumLabel.setText(QCoreApplication.translate("PokemonPopup", u"atk", None))
        self.defNumLabel.setText(QCoreApplication.translate("PokemonPopup", u"def", None))
        self.spaNumLabel.setText(QCoreApplication.translate("PokemonPopup", u"spa", None))
        self.spdNumLabel.setText(QCoreApplication.translate("PokemonPopup", u"spd", None))
        self.speNumLabel.setText(QCoreApplication.translate("PokemonPopup", u"spe", None))
        self.label.setText(QCoreApplication.translate("PokemonPopup", u"Moveset", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("PokemonPopup", u"Search move...", None))
    # retranslateUi

