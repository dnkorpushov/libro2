
from PyQt5.QtWidgets import (QDialogButtonBox, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QLineEdit, 
                             QCheckBox, QComboBox)
from PyQt5.QtCore import QCoreApplication, QSize
from plugin_collection import Param
from .customcontrols import FolderPicker, FilePicker
from .smartdialog import SmartDialog

_t = QCoreApplication.translate

class PluginForm(SmartDialog):
    def __init__(self, parent, params, title):
        super().__init__(parent)
        self.params = params
        self.setWindowTitle(title)
        base_width = 350 
        base_height = 80 

        self.setMinimumSize(QSize(int(base_width * self.scale_factor()), int(base_height * self.scale_factor())))  
        self.resize(self.minimumSize())
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)

        if len(self.params) == 0:
            label = QLabel(_t('plugin', 'Run plugin?'))
            label.setWordWrap(True)
            self.layout.addWidget(label)
        else:
            for param in self.params:
                if param.type == Param.Text:
                    label = QLabel(param.title)
                    self.layout.addWidget(label)

                    control = QLineEdit()
                    control.setObjectName(param.name)
                    control.setText(str(param.default_value))
                    self.layout.addWidget(control)

                elif param.type == Param.Boolean:
                    control = QCheckBox(self)
                    control.setText(param.title)
                    control.setObjectName(param.name)
                    if param.default_value:
                        control.setChecked(param.default_value)
                    else:
                        control.setChecked(False)
                    self.layout.addWidget(control)

                elif param.type == Param.Choice:
                    label = QLabel(param.title)
                    self.layout.addWidget(label)
                    control = QComboBox(self)
                    control.setObjectName(param.name)
                    for item in param.default_value:
                        control.addItem(item)
                    control.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                    self.layout.addWidget(control)

                elif param.type == Param.Folder:
                    label = QLabel(param.title)
                    self.layout.addWidget(label)

                    control = FolderPicker(self)
                    control.setObjectName(param.name)
                    if param.default_value:
                        control.setText(param.default_value)
                    self.layout.addWidget(control)

                elif param.type == Param.File:
                    label = QLabel(param.title)
                    self.layout.addWidget(label)

                    control = FilePicker(self)
                    control.setObjectName(param.name)
                    if param.default_value:
                        control.setText(param.default_value)
                    self.layout.addWidget(control)
                
        self.spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(self.spacer)
        self.buttons = QDialogButtonBox(self)
        self.buttons.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)
        self.adjustSize()


    def getParams(self):
        for widget in self.children():
            value = None
            object_name = widget.objectName()
            if isinstance(widget, QLineEdit) or isinstance(widget, FilePicker) or isinstance(widget, FolderPicker):
                value = widget.text()
            elif isinstance(widget, QCheckBox):
                value = widget.isChecked()
            elif isinstance(widget, QComboBox):
                value = widget.currentText()
          
            for param in self.params:
                if param.name == object_name:
                    param.value = value
        
        return self.params

    def _save_size(self):
        return


           

