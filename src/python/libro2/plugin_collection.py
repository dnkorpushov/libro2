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

class MetaPlugin:
    def __init__(self):
        self._description = 'UNKNOWN'

    def description(self):
        return self._description

    def perform_operation(self, meta):
        raise NotImplementedError('Method "preform_operation" not implemented')

class FilePlugin:
    def __init__(self):
        self._description = 'UNKNOWN'

    def description(self):
        return self._description
    
    def perform_operation(self, file_list):
        raise NotImplementedError('Method "preform_operation" not implemented')