import traceback
from functools import partial
from PyQt5.QtWidgets import (QDialogButtonBox, QVBoxLayout, QLabel,
                             QSpacerItem, QSizePolicy, QLineEdit,
                             QCheckBox, QComboBox)
from PyQt5.QtCore import QCoreApplication, QSize
from .customcontrols import FolderPicker, FilePicker
from .smartdialog import SmartDialog
from ui.textviewdialog import TextViewDialog
from plugin_collection import (TextField, BoolField, ChoiceField, FileField, 
                               FolderField)


_t = QCoreApplication.translate


class PluginForm(SmartDialog):
    def __init__(self, parent, plugin):
        super().__init__(parent)
        self.plugin = plugin
        self.form_attrs = {}
        self.__init = True
        self.setWindowTitle(plugin.title())
        base_width = 350
        base_height = 80

        self.setMinimumSize(
            QSize(
                int(base_width * self.scale_factor()),
                int(base_height * self.scale_factor())
                )
            )
        self.resize(self.minimumSize())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)

        for attr_key in self.plugin.__dict__.keys():
            attr = getattr(self.plugin, attr_key)
            label = None
            widget = None

            if isinstance(attr, TextField):
                label = QLabel(attr.label)
                widget = QLineEdit()
                widget.textChanged.connect(
                    partial(self.valueChanged, attr_key))

            elif isinstance(attr, BoolField):
                widget = QCheckBox(attr.label, self)
                widget.stateChanged.connect(
                    partial(self.valueChanged, attr_key))

            elif isinstance(attr, ChoiceField):
                label = QLabel(attr.label)
                widget = QComboBox(self)
                for item in attr.items:
                    widget.addItem(item, userData=item)
                widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                widget.currentIndexChanged.connect(
                    partial(self.valueChanged, attr_key))

            elif isinstance(attr, FileField):
                label = QLabel(attr.label)
                widget = FilePicker(self)
                widget.textChanged.connect(
                    partial(self.valueChanged, attr_key))

            elif isinstance(attr, FolderField):
                label = QLabel(attr.label)
                widget = FolderPicker(self)
                widget.textChanged.connect(
                    partial(self.valueChanged, attr_key))

            if label is not None:
                self.layout.addWidget(label)
                label.setObjectName(attr_key + '_label')
            if widget is not None:
                self.layout.addWidget(widget)
                widget.setObjectName(attr_key)
                self.form_attrs[attr_key] = attr

        if len(self.form_attrs) == 0:
            label = QLabel(_t('plugin', 'Run plugin?'))
            label.setWordWrap(True)
            self.layout.addWidget(label)

        self.getPluginAttributesValue()
        self.setWidgetsStatus()

        self.__init = False

        self.spacer = QSpacerItem(20, 20, QSizePolicy.Minimum,
                                  QSizePolicy.Expanding)
        self.layout.addItem(self.spacer)
        self.buttons = QDialogButtonBox(self)
        self.buttons.setStandardButtons(QDialogButtonBox.Ok |
                                        QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)
        self.adjustSize()

    def valueChanged(self, param_name):
        if not self.__init:
            try:
                self.setPluginAttributesValue()
                self.plugin.validate(self.form_attrs[param_name])
                self.getPluginAttributesValue()
                self.setWidgetsStatus()
            except Exception:
                errorDialog = TextViewDialog(self, [{ 'src': None, 'dest': None, 'error': traceback.format_exc()}])
                errorDialog.exec()

    def setPluginAttributesValue(self):
        for attr_name in self.form_attrs.keys():
            self.form_attrs[attr_name].value = self.getWidgetValue(attr_name)

    def getPluginAttributesValue(self):
        for attr_name in self.form_attrs.keys():
            self.setWidgetValue(attr_name, self.form_attrs[attr_name].value)

    def setWidgetsStatus(self):
        for attr_name in self.form_attrs.keys():
            widget = self.getWidget(attr_name)
            label = self.getWidget(attr_name + '_label')
            if widget:
                widget.setVisible(self.form_attrs[attr_name].visible)
                widget.setEnabled(self.form_attrs[attr_name].enabled)
            if label:
                label.setVisible(self.form_attrs[attr_name].visible)

    def setWidgetValue(self, attr_name, value):
        for widget in self.children():
            if widget.objectName() == attr_name:
                if isinstance(widget, (QLineEdit, FilePicker, FolderPicker)):
                    if value:
                        widget.setText(str(value))
                    else:
                        widget.setText('')
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))
                elif isinstance(widget, QComboBox):
                    index = widget.findData(value)
                    if index != -1:
                        widget.setCurrentIndex(index)
                break

    def getWidgetValue(self, attr_name):
        value = None
        for widget in self.children():
            if widget.objectName() == attr_name:
                if isinstance(widget, (QLineEdit, FilePicker, FolderPicker)):
                    value = widget.text()
                elif isinstance(widget, QCheckBox):
                    value = widget.isChecked()
                elif isinstance(widget, QComboBox):
                    value = widget.currentText()
                break

        return value

    def getWidget(self, attr_name):
        for widget in self.children():
            if widget.objectName() == attr_name:
                return widget

        return None

    def accept(self):
        try:
            self.setPluginAttributesValue()
            self.plugin.validate(source=None)
            return super().accept()

        except Exception:
            errorDialog = TextViewDialog(self, [{ 'src': None, 'dest': None, 'error': traceback.format_exc()}])
            errorDialog.exec()

    def _save_size(self):
        return


           

