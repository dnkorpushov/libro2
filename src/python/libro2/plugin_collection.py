import os
import sys
import importlib
import inspect
import traceback

import config
settings = config.settings


class AbstractField:
    def __init__(self, value=None, label=None):
        self.value = value
        self.label = label
        self.enabled = True
        self.visible = True


class TextField(AbstractField):
    pass


class BoolField(AbstractField):
    pass


class ChoiceField(AbstractField):
    def __init__(self, value=None, label=None, items=[]):
        super().__init__(value=value, label=label)
        self.items = items
        self.value = items[0] if len(items) > 0 else None


class FolderField(AbstractField):
    pass


class FileField(AbstractField):
    pass


class DebugException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class PluginCollection:
    def __init__(self):
        self.plugins_path = []

        if getattr(sys, 'frozen', False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(__file__)
        sys_plugins_path = os.path.join(app_path, 'plugins')

        if not os.path.exists(config.plugins_path):
            os.makedirs(config.plugins_path)

        sys.path.append(sys_plugins_path)
        sys.path.append(config.plugins_path)

        self.plugins_path.append(sys_plugins_path)
        self.plugins_path.append(config.plugins_path)

        self.reload_plugins()

    def reload_plugins(self):
        self._plugins = []
        self.errors = []
        for plugins_path in self.plugins_path:
            for file in os.listdir(plugins_path):
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

                    except Exception:
                        self.errors.append({'src': f'Plugin {file}', 'dest': None, 'error': traceback.format_exc()})

    def plugins(self):
        return self._plugins


class AbstractPlugin:
    def __init__(self):
        self._title = None
        self._description = None
        self._hotkey = None
        self._is_context_menu = False

    def init(self):
        return

    def validate(self, source=None):
        return

    def title(self):
        return self._title

    def description(self):
        return self._description

    def hotkey(self):
        return self._hotkey

    def is_context_menu(self):
        return self._is_context_menu

    def load_settings(self, key, default_value=None):
        if key in settings.plugin_settings.keys():
            return settings.plugin_settings[key]
        else:
            return default_value

    def save_settings(self, key, value):
        settings.plugin_settings[key] = value


class MetaPlugin(AbstractPlugin):
    def init(self):
        self._title = 'MetaPlugin Class'

    def perform_operation(self, meta):
        raise NotImplementedError('Method "preform_operation" not implemented')


class FilePlugin(AbstractPlugin):
    def init(self):
        self._title = 'FilePlugin Class'
 
    def perform_operation(self, file_list):
        raise NotImplementedError('Method "preform_operation" not implemented')