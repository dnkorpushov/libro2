# Плагин архивирует файл *.fb2 в файл *.fb2.zip

from plugin_collection import FilePlugin, DebugException, Param
from ebookmeta.myzipfile import ZipFile, ZIP_DEFLATED
import os


class ZipFb2(FilePlugin):
    def __init__(self):
        super().__init__()
        self._description = 'Архивировать fb2 в fb2.zip'
        self.add_param(name='delete_source', 
                       type=Param.Boolean, 
                       title='Удалить исходные файлы после архивации',
                       default_value=False)

    def perform_operation(self, file):
        delete_source = self.get_param('delete_source')
        if file.lower().endswith('.fb2'):
            file_path = os.path.dirname(file)
            file_name = os.path.basename(file)
            zip_name = file + '.zip'

            if not os.path.exists(zip_name):
                os.chdir(file_path)
                zip = ZipFile(zip_name, mode='w', compression=ZIP_DEFLATED)
                zip.write(file_name)
                zip.close()
                
                # if delete_source:
                #     os.remove(file)

                return zip_name
            else:
                raise DebugException(f'Файл "{zip_name}" уже существует!')
        else:
            if file.lower().endswith('.fb2.zip'):
                raise DebugException(f'"{file}" уже заархивирован в fb2.zip.')
            else:
                raise DebugException(f'"{file}" не является файлом fb2!')

