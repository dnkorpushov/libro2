import ebookmeta
import lxml
import os
import sys
import importlib
import inspect
import traceback

import config

class DebugException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

class PluginCollection:
    def __init__(self):
        self.plugin_path = config.plugins_path
        if not os.path.exists(self.plugin_path):
            os.makedirs(self.plugin_path)
        sys.path.append(self.plugin_path)

        self.reload_plugins()

    def reload_plugins(self):
        self._plugins = []
        self.errors = []
        for file in os.listdir(self.plugin_path):
            if file.lower().endswith('.py'):
                
                try:
                    module_name, _ = os.path.splitext(os.path.basename(file))
                    plugin_module = importlib.__import__(module_name)
                    importlib.reload(plugin_module)

                    clsmembers = inspect.getmembers(plugin_module, inspect.isclass)

                    for (_, c) in clsmembers:
                        if (
                                (issubclass(c, MetaPlugin) or issubclass(c, FilePlugin)) 
                                and c is not MetaPlugin and c is not FilePlugin
                            ):
                            self._plugins.append(c())

                except Exception as e:
                    self.errors.append({'src': f'Plugin {file}', 'dest': None, 'error': traceback.format_exc()})

    def plugins(self):
        return self._plugins


class Param:
    Text = 0
    Boolean = 1
    Folder = 2
    File = 3
    Choice = 4

    def __init__(self, name, type, title, default_value):
        if default_value:
            if type == Param.Boolean and not isinstance(default_value, bool):
                raise Exception(f'Boolean parameter "{name}" has wrong default value type')
            elif type == Param.Text and not isinstance(default_value, str):
                raise Exception(f'Text parameter "{name}" has wrong default value type')
            elif type == Param.Folder and not isinstance(default_value, str):
                raise Exception(f'Folder parameter "{name}" has wrong default value type')
            elif type == Param.File and not isinstance(default_value, str):
                raise Exception(f'File parameter "{name}" has wrong default value type')
            elif type == Param.Choice and not isinstance(default_value, list):
                raise Exception(f'Choice parameter "{name}" has wrong default value type')

        self.name = name
        self.type = type
        self.title = title
        self.default_value = default_value
        self.value = None


class AbstractPlugin:
    def __init__(self):
        self._params = []
        self._description = None
        self._hotkey = None
        self._is_context_menu = False
        self.init()

    def init(self):
        pass

    def description(self):
        return self._description

    def hotkey(self):
        return self._hotkey

    def is_context_menu(self):
        return self._is_context_menu

    def add_param(self, name, type, title, default_value=None):
        param = Param(name=name, type=type, title=title, default_value=default_value)
        self._params.append(param)
    
    def get_param(self, name):
        
        for param in self._params:
            if param.name == name:
                return param

        raise Exception(f'Parameter "{name}" not found!')

    def params(self):
        return self._params
    
    def set_params(self, params):
        self._params = params

class MetaPlugin(AbstractPlugin):
    def init(self):
        self._description = 'Meta Plugin'

    def perform_operation(self, meta):
        raise NotImplementedError('Method "preform_operation" not implemented')


class FilePlugin(AbstractPlugin):
    def init(self):
        self._description = 'File Plugin'
    
    def perform_operation(self, file_list):
        raise NotImplementedError('Method "preform_operation" not implemented')