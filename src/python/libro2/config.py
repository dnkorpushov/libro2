import os
import sys
import json
import codecs
from types import SimpleNamespace

if sys.platform == 'win32':
    config_folder_name = 'libro2'
else:
    config_folder_name = '.libro2'

config_path = os.path.join(os.path.expanduser('~'), config_folder_name)
config_file = os.path.join(config_path, 'settings.json')
database_name = os.path.join(config_path, 'libro2.db')


settings = SimpleNamespace(
    add_folder_last_selected=os.path.expanduser('~'),
    add_files_last_selected=os.path.expanduser('~'),
    ui_window_x=None,
    ui_window_y=None,
    ui_window_width=None,
    ui_window_height=None,   
    ui_info_panel_visible=True,
    ui_filter_panel_visible=True,
    ui_toolbar_visible=True,
    ui_toolbar_icon_size='large',
    ui_auto_apply_filter=True, 
    ui_splitter_sizes=[], 
    ui_columns_width=[],
    ui_columns_order=[],
    ui_hidden_columns=[],
    ui_hidden_columns_width=[],
    rename_author_format='#l{ #f}',
    rename_filename_format='#author. #title',
    rename_delete_source_files=False,
    rename_backup=True,
    rename_overwrite=False,
    convert_converter_path=None,
    convert_converter_config=None,
    convert_output_format = None,
    convert_output_path=None,
    convert_overwrite=False
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
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    if os.path.exists(config_file):
        with codecs.open(config_file, 'r', encoding='utf-8') as f:
            c = json.loads(f.read())
    
        for key in c:
            settings.__dict__[key] = c[key]

