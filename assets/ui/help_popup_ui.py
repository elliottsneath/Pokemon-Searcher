# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'help_popup.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_helpDialog(object):
    def setupUi(self, helpDialog):
        if not helpDialog.objectName():
            helpDialog.setObjectName(u"helpDialog")
        helpDialog.resize(399, 326)
        self.verticalLayout = QVBoxLayout(helpDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(helpDialog)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(helpDialog)

        QMetaObject.connectSlotsByName(helpDialog)
    # setupUi

    def retranslateUi(self, helpDialog):
        helpDialog.setWindowTitle(QCoreApplication.translate("helpDialog", u"Help", None))
        self.label.setText(QCoreApplication.translate("helpDialog", u"Developed by Elliott Sneath\n"
"GitHub: elliottsneath\n"
"Discord: vapelordell\n"
"\n"
"Welcome to the Pok\u00e9mon Searcher!\n"
"\n"
"To choose a selection of pok\u00e9mon, visit the settings page, and either manually select pok\u00e9mon from the list, or import a list of pok\u00e9mon from a file. This includes using a .pkmlist file or a Google Sheet draft doc.\n"
"\n"
"To import from a draft doc, download a copy as a .xlsx, and make sure the sheet with the necessary pok\u00e9mon on is called \"Board\". Once your selection has been made, if you wish to share, you can export your list to a .pkmnlist file in settings, which can be shared to other players in the draft league etc.\n"
"\n"
"When importing from a draft board, pok\u00e9mon under the column header \"Banned\" will be ignored.\n"
"\n"
"The Current Draft page shows your drafted team alongside a live team analysis. The type weakness, resistance, and immunity panels update automatically as you add pok\u00e9mon. Set your total budget and number of picks in the settings bar to enable recommendations \u2014 the tool will suggest the best available pok\u00e9mon based on missing team roles (such as Stealth Rock, Bulky Water, or Grounded Poison) and type coverage. Recommendations are hidden when you have no points remaining.", None))
    # retranslateUi

