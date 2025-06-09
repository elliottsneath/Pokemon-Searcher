# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_popup.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

from assets.ui.animated_button import AnimatedHoverButton

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(533, 323)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.textEdit = QTextEdit(Form)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fromFileButton = AnimatedHoverButton(Form)
        self.fromFileButton.setObjectName(u"fromFileButton")

        self.horizontalLayout.addWidget(self.fromFileButton)

        self.fromGoogleSheetButton = AnimatedHoverButton(Form)
        self.fromGoogleSheetButton.setObjectName(u"fromGoogleSheetButton")

        self.horizontalLayout.addWidget(self.fromGoogleSheetButton)

        self.fromPlainTextButton = AnimatedHoverButton(Form)
        self.fromPlainTextButton.setObjectName(u"fromPlainTextButton")

        self.horizontalLayout.addWidget(self.fromPlainTextButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Paste a URL to a draft league sheet, or a list of pok\u00e9mon. See the \"Help\" tab for more information", None))
        self.textEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Type Pok\u00e9mon List here...", None))
        self.fromFileButton.setText(QCoreApplication.translate("Form", u"Import from .pkmnlist", None))
        self.fromGoogleSheetButton.setText(QCoreApplication.translate("Form", u"Import from Draft doc", None))
        self.fromPlainTextButton.setText(QCoreApplication.translate("Form", u"Import from plain text", None))
    # retranslateUi

