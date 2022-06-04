import os
import json
import codecs

config_file = os.path.join(os.path.expanduser('~'), 'libro2', 'settings.json')

add_folder_last_selected = None
add_files_last_selected = None

ui_window_x = None
ui_window_y = None
ui_window_width = None
ui_window_height = None
ui_info_panel_visible = True
ui_filter_panel_visible = True
ui_auto_apply_filter = True
ui_splitter_sizes = []


def save():
    global add_folder_last_selected
    global add_files_last_selected
    global ui_window_x
    global ui_window_y 
    global ui_window_width
    global ui_window_height
    global ui_info_panel_visible
    global ui_filter_panel_visible
    global ui_auto_apply_filter
    global ui_splitter_sizes

    c = {
            'add_folder_last_selected': add_folder_last_selected,
            'add_files_last_selected': add_files_last_selected,
            'ui_window_x': ui_window_x,
            'ui_window_y': ui_window_y,
            'ui_window_width': ui_window_width,
            'ui_window_height': ui_window_height,
            'ui_info_panel_visible': ui_info_panel_visible,
            'ui_filter_panel_visible': ui_filter_panel_visible,
            'ui_auto_apply_filter': ui_auto_apply_filter,
            'ui_splitter_sizes': ui_splitter_sizes

        }

    (config_dir, _) = os.path.split(config_file)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        
    with codecs.open(config_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(c, sort_keys=False, indent=4))


def load( ):
    global add_folder_last_selected
    global add_files_last_selected
    global ui_window_x
    global ui_window_y 
    global ui_window_width
    global ui_window_height
    global ui_info_panel_visible
    global ui_filter_panel_visible
    global ui_auto_apply_filter
    global ui_splitter_sizes

    if os.path.exists(config_file):
        with codecs.open(config_file, 'r', encoding='utf-8') as f:
            c = json.loads(f.read())

            add_folder_last_selected = c.get('add_folder_last_selected', os.path.expanduser('~'))
            add_files_last_selected = c.get('add_files_last_selected', os.path.expanduser('~'))
            ui_window_x = c.get('ui_window_x', None)
            ui_window_y = c.get('ui_window_y', None)
            ui_window_width = c.get('ui_window_width', None)
            ui_window_height = c.get('ui_window_height', None)
            ui_info_panel_visible = c.get('ui_info_panel_visible', True)
            ui_filter_panel_visible = c.get('ui_filter_panel_visible', True)
            ui_auto_apply_filter = c.get('ui_auto_apply_filter', True)
            ui_splitter_sizes = c.get('ui_splitter_sizes', [])
