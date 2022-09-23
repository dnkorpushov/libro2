# Automatic series index creation
from plugin_collection import MetaPlugin, DebugException, Param
from config import locale, settings

class SeriesIndexer(MetaPlugin):
    def init(self):
        default_title = self.load_settings('SeriesIdx.Title', default_value='')
        start_index = self.load_settings('SeriesIdx.StartValue', default_value='1')
        self.start_index = int(start_index)

        if locale == 'ru_RU':
            self._title = 'Автоматическая нумерация серии'
            self._description = 'Плагин нумерует серию в выбранных книгах согласно сортировке в списке'
            
            self.add_param(name='series_title',
                           title='Название серии (опционально)',
                           type=Param.Text,
                           default_value=default_title)
            self.add_param(name='series_index_start',
                           title='Начинать индексирование с',
                           type=Param.Text,
                           default_value=start_index)
        else:
            self._title = 'Series index generator'
            self._description = 'Generate series index in book sort order'

            self.add_param(name='series_title',
                           title='Series title (optional)',
                           type=Param.Text,
                           default_value='')
            self.add_param(name='series_index_start',
                           title='Series index start value',
                           type=Param.Text,
                           default_value='1')            

    def validate(self):
        start_value = self.get_param('series_index_start').value
        title = self.get_param('series_title').value
        try:
            self.start_index = int(start_value)
            self.save_settings('SeriesIdx.Title', value=title)
            self.save_settings('SeriesIdx.StartValue', value=start_value)
        except:
            if locale == 'ru_RU':
                raise DebugException('Неверно значение начального индекса!')
            else:
                raise DebugException('Wrong series index start value!')

    def perform_operation(self, meta):
        if self.get_param('series_title').value:
            meta.series = self.get_param('series_title').value
        meta.series_index = self.start_index
        self.start_index += 1

        return meta
