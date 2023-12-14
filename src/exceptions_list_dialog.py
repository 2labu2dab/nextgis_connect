from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QLabel, QScrollArea, QSizePolicy, QVBoxLayout, QWidget,
)

from qgis.core import Qgis, QgsMessageLog


def qgisLog(msg, level=Qgis.MessageLevel.Info):
    QgsMessageLog.logMessage(msg, 'NextGIS Connect', level)


class ExceptionsListDialog(QDialog):

    def __init__(self, title, parent):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.resize(400, 200)
        self.setLayout(QVBoxLayout())

        self.exceptionsList = QWidget()
        self.exceptionsContainer = QVBoxLayout(self.exceptionsList)
        self.scroll = QScrollArea()
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.scroll.setWidget(self.exceptionsList)
        self.scroll.setWidgetResizable(True)

        self.layout().addWidget(self.scroll)
        self.layout().setContentsMargins(0,0,0,0)

        self.buffer = QLabel()
        self.buffer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.exceptionsContainer.insertWidget(0, self.buffer)

    def addException(self, msg, w_msg_deteils, icon):
        self.exceptionsContainer.insertWidget(0, ExceptionWidget(msg, w_msg_deteils, icon, self))


class ExceptionWidget(QFrame):

    def __init__(self, msg, w_msg_deteils, icon, parent):
        super().__init__(parent)

        self.msg = msg

        self.setStyleSheet(
            """
                ExceptionWidget{
                    border: 1px solid #d9d9d9;
                    border-top-color: transparent;
                    border-left-color: transparent;
                    border-right-color: transparent;
                }
            """
        )

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,6,0,9)

        self.iconLabel = QLabel()
        self.iconLabel.setObjectName("iconLabel")
        pm = QPixmap(icon)
        self.iconLabel.setPixmap(pm.scaledToWidth(8))
        self.iconLabel.resize(8, 8)
        self.iconLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.iconWidget = QWidget()
        self.iconWidget.setObjectName("iconWidget")
        self.iconWidget.setLayout(QVBoxLayout())
        self.iconWidget.layout().addWidget(self.iconLabel, 0, Qt.AlignHCenter | Qt.AlignTop)
        self.iconWidget.layout().setContentsMargins(0,3,3,0)
        self.iconWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        self.infoWidget = QWidget()
        self.infoWidget.setLayout(QVBoxLayout())
        self.infoWidget.layout().setContentsMargins(0,0,0,0)

        self.msgLabel = QLabel(msg)
        self.msgLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.msgLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.msgLabel.setWordWrap(True)
        self.infoWidget.layout().addWidget(self.msgLabel)

        if w_msg_deteils is not None:
            self.fullMsgLabel = QLabel(w_msg_deteils)
            self.fullMsgLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.fullMsgLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.fullMsgLabel.setWordWrap(True)
            self.fullMsgLabel.setStyleSheet("font-size: %dpt" % (self.msgLabel.font().pointSize() - 1))
            self.infoWidget.layout().addWidget(self.fullMsgLabel)

        self.layout().addWidget(self.iconWidget)
        self.layout().addWidget(self.infoWidget)
