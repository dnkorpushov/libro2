# Плагин копирует файл в файл с именем "Автор - Название"
from plugin_collection import FilePlugin, DebugException

import os
import shutil
import ebookmeta


class SamplePlugin(FilePlugin):
    def __init__(self):
        super().__init__()
        self._description = 'Копировать в "Автор - Название"'
    
    def description(self):
        return self._description


    def perform_operation(self, file):
        meta = ebookmeta.get_metadata(file)
        new_file_name = meta.get_filename_by_pattern('#Author - #Title', '{#f }#l')
        
        base_dir = os.path.dirname(file)
        new_file = os.path.join(base_dir, new_file_name)

        if not os.path.exists(new_file):
            shutil.copy(file, new_file)
        else:
            raise DebugException(f'Файл "{new_file}" уже существует!')
        return new_file

