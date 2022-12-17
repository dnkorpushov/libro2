# Remove middle name for each author in authors list
from plugin_collection import MetaPlugin
from config import locale


class RemoveAuthorMiddleName(MetaPlugin):
    def init(self):
        if locale == 'ru_RU':
            self._title = 'Удалить отчество у автора'
            self._description = ('Некотрые предпочитают в библиотеке видеть '
                                 'автора в формате "Имя Фамилия" вместо '
                                 '"Иия Отчество Фамилия". Например, Виктор '
                                 'Пелевин вместо Виктор Олегович Пелевин. '
                                 'Данный плагин удаляет отчество у автора, '
                                 'если оно присутствует.')
        else:
            self._title = 'Remove author\'s middle name'
            self._description = ('Remove middle name for each author'
                                 'in authors list')

    def perform_operation(self, meta):
        new_authors = []

        for author in meta.author_list:
            author_part = author.split()
            if len(author_part) == 3: # Author have middle name
                new_author = author_part[0] + ' ' + author_part[2]
                new_authors.append(new_author)
            else:
                new_authors.append(author)

        meta.set_author_list_from_string(','.join(new_authors))

        return meta

