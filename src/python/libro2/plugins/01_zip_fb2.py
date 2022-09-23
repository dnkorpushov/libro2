# Плагин архивирует файл *.fb2 в файл *.fb2.zip

from plugin_collection import FilePlugin, DebugException, Param
from ebookmeta.myzipfile import ZipFile, ZIP_DEFLATED
import os
from config import locale


class ZipFb2(FilePlugin):
    def init(self):
        if locale == 'ru_RU':
            self._title = 'Упаковать fb2 в fb2.zip'
            self._description = 'Преобразовывает файлы fb2 в формат fb2.zip. Если указано, после преобразования исходный fb2 удаляется.'
            self._hotkey = 'Ctrl+Z'
            self._is_context_menu = True

            self.add_param(name='delete_source', 
                           type=Param.Boolean, 
                           title='Удалить исходные файлы после архивации',
                           default_value=False)
        else:
            self._title = 'Zip fb2 into fb2.zip'
            self._description = 'Zip fb2 files into fb2.zip, then delete original fb2, if specified.'
            self._hotkey = 'Ctrl+Z'
            self._is_context_menu = True

            self.add_param(name='delete_source', 
                           type=Param.Boolean, 
                           title='Delete original fb2 after zipping',
                           default_value=False)

    def perform_operation(self, file):
        if file.lower().endswith('.fb2'):
            file_path = os.path.dirname(file)
            file_name = os.path.basename(file)
            zip_name = file + '.zip'

            if not os.path.exists(zip_name):
                os.chdir(file_path)
                zip = ZipFile(zip_name, mode='w', compression=ZIP_DEFLATED)
                zip.write(file_name)
                zip.close()
                
                if self.get_param('delete_source').value:
                    os.remove(file)

                return zip_name
            else:
                if locale == 'ru_RU':
                    raise DebugException(f'Файл "{zip_name}" уже существует!')
                else:
                    raise DebugException(f'File "{zip_name}" already exist!')
        else:
            if file.lower().endswith('.fb2.zip'):
                if locale == 'ru_RU':
                    raise DebugException(f'"{file}" уже упакован в fb2.zip.')
                else:
                    raise DebugException(f'"{file}" zipped already.')
            else:
                if locale == 'ru_RU':
                    raise DebugException(f'"{file}" не является файлом fb2!')
                else:
                    raise DebugException(f'"{file}" not fb2 file!')

