from . import _ApplicationContext, _QtBinding, cached_property
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtNetwork import QAbstractSocket


class ApplicationContext(_ApplicationContext):
    @cached_property
    def _qt_binding(self):
        return _QtBinding(QApplication, QIcon, QAbstractSocket)
