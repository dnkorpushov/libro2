# Плагин архивирует файл *.fb2 в файл *.fb2.zip

from plugin_collection import FilePlugin, DebugException
from ebookmeta.myzipfile import ZipFile, ZIP_DEFLATED
import os


class ZipFb2(FilePlugin):
    def __init__(self):
        super().__init__()
        self._description = 'Архивировать файлы fb2'

    def description(self):
        return self._description

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
                
                return zip_name
            else:
                raise DebugException(f'Файл "{zip_name}" уже существует!')
        else:
            raise DebugException(f'"{file}" не является файлом fb2!')

