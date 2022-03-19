from . import _ApplicationContext, _QtBinding, cached_property
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from PySide2.QtNetwork import QAbstractSocket


class ApplicationContext(_ApplicationContext):
    @cached_property
    def _qt_binding(self):
        return _QtBinding(QApplication, QIcon, QAbstractSocket)
