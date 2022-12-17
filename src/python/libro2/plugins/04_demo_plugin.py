from plugin_collection import (MetaPlugin, TextField, BoolField,
                               ChoiceField, FolderField, FileField,
                               DebugException)


class TestPlugin(MetaPlugin):
    def init(self):
        self._title = 'Демонстрационный плагин'
        self._description = 'Проверка работы плагина'

        self.text_field = TextField(label='Текстовое поле')
        self.bool_field = BoolField(
            label='Логическое поле (разрешить/запретить выбор из списка)'
        )
        self.choice_field = ChoiceField(label='Выбор из списка')
        self.hide_file_field = BoolField(label='Скрыть/показать выбор файла')
        self.file_field = FileField(label='Выбор файла')
        self.folder_field = FolderField(label='Выбор папки')

        self.text_field.value = 'Привет'
        self.bool_field.value = True
        self.hide_file_field.value = False
        self.choice_field.items = ['Один', 'Два', 'Три']
        self.choice_field.value = 'Два'
        self.file_field.value = 'file.fb2'
        self.folder_field.value = 'c:/work/books'

        self.choice_field.enabled = True

    def validate(self, source):
        if source == self.bool_field:
            self.choice_field.enabled = self.bool_field.value

        elif source == self.hide_file_field:
            self.file_field.visible = not self.hide_file_field.value

        elif source == self.text_field:
            self.file_field.value = self.text_field.value

        elif source is None:
            raise DebugException('Final validate')

    def perform_operation(self, meta):
        pass
