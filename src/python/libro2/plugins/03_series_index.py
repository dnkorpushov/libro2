# Automatic series index creation
from plugin_collection import MetaPlugin, DebugException, TextField
from config import locale


class SeriesIndexer(MetaPlugin):
    def init(self):
        default_title = self.load_settings('SeriesIdx.Title', default_value='')
        start_index = self.load_settings('SeriesIdx.StartValue',
                                         default_value='1')

        self.series_title = TextField()
        self.series_index_start = TextField()

        self.series_title.value = default_title
        self.series_index_start.value = int(start_index)

        if locale == 'ru_RU':
            self._title = 'Автоматическая нумерация серии'
            self._description = ('Плагин нумерует серию в выбранных книгах '
                                 'согласно сортировке в списке')
            self.series_title.label = 'Название серии (опционально)'
            self.series_index_start.label = 'Начинать индексирование с'
        else:
            self._title = 'Series index generator'
            self._description = 'Generate series index in book sort order'

            self.series_title.label = 'Series title (optional)'
            self.series_index_start.label = 'Series index start value'

    def validate(self, source):
        if source is None:
            try:
                self.start_index = int(self.series_index_start.value)
                self.save_settings('SeriesIdx.Title',
                                   value=self.series_title.value)
                self.save_settings('SeriesIdx.StartValue',
                                   value=self.start_index)
            except ValueError:
                if locale == 'ru_RU':
                    raise DebugException(
                        'Неверное значение начального индекса!')
                else:
                    raise DebugException('Wrong series index start value!')

    def perform_operation(self, meta):
        if self.series_title.value:
            meta.series = self.series_title.value
        meta.series_index = self.start_index
        self.start_index += 1

        return meta
