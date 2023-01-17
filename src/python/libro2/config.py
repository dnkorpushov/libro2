import os
import sys
import json
import codecs
import tempfile
import shutil
from types import SimpleNamespace


def get_app_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(__file__)


if sys.platform == 'win32':
    config_folder_name = 'libro2'
else:
    config_folder_name = '.libro2'

app_path = get_app_path()

temp_dir = tempfile.mkdtemp(prefix='libro2_')

portable = False
portable_converter_path = None
portable_converter_config = None

if os.path.exists(os.path.join(app_path, 'portable')):
    config_path = app_path
    portable = True
else:
    config_path = os.path.join(os.path.expanduser('~'), config_folder_name)

config_file = os.path.join(config_path, 'settings.json')
plugins_path = os.path.join(config_path, 'plugins')
database_name = os.path.join(temp_dir, 'libro2.db')
locale = None

settings = SimpleNamespace(
    add_folder_last_selected=os.path.expanduser('~'),
    add_files_last_selected=os.path.expanduser('~'),
    ui_window_x=None,
    ui_window_y=None,
    ui_window_width=None,
    ui_window_height=None,
    ui_info_panel_visible=True,
    ui_filter_panel_visible=True,
    ui_auto_apply_filter=True,
    ui_cover_image_width=110,
    ui_splitter_sizes=[],
    ui_columns_width=[],
    ui_columns_order=[],
    ui_hidden_columns=[],
    ui_hidden_columns_width=[],
    ui_dialog_size={},
    is_open_folder_on_start=False,
    open_folder_on_start=None,
    reader_app_fb2=None,
    reader_app_epub=None,
    rename_in_source_folder=True,
    rename_move_to_folder=os.path.expanduser('~'),
    rename_author_format='{lastname} {f}',
    rename_translator_format='{lastname}',
    rename_filename_format='{author}. {title}',
    rename_delete_source_files=False,
    rename_backup=True,
    rename_overwrite=False,
    rename_author_template_list=[],
    rename_translator_template_list=[],
    rename_filename_template_list=[],
    rename_path_list=[],
    convert_path_list=[],
    convert_converter_path=None,
    convert_converter_config=None,
    convert_output_format=None,
    convert_in_source_folder=False,
    convert_output_path=None,
    convert_overwrite=False,
    convert_stk=False,
    plugin_settings={}
)


def init():
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    if os.path.exists(database_name):
        os.unlink(database_name)


def save():
    (config_dir, _) = os.path.split(config_file)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    with codecs.open(config_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(settings.__dict__, sort_keys=False, indent=4))


def load():
    global portable_converter_path, portable_converter_config

    if not os.path.exists(config_path):
        os.makedirs(config_path)

    if os.path.exists(config_file):
        with codecs.open(config_file, 'r', encoding='utf-8') as f:
            c = json.loads(f.read())

        for key in c:
            settings.__dict__[key] = c[key]
       

def get_rel_path(path):
    if portable:
        return os.path.abspath(os.path.join(app_path, path))
    else:
        return path


def delete_temp_dir():
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

