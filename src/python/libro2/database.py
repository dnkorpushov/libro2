import os
import traceback
import ebookmeta
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtCore import QByteArray
import query as query
from types import SimpleNamespace
import config

db = QSqlDatabase.addDatabase('QSQLITE')


def init():
    db.setDatabaseName(config.database_name)

    db.open()
    if not is_created():
        create()


def is_created():
    rows = -1
    q = QSqlQuery(db)
    q.exec(query.check_db_created)
    if q.next():
        rows = q.value(0)

    return rows == 1


def create():
    q = QSqlQuery(db)
    sql_lines = query.create_tables.split(';')
    for line in sql_lines:
        if len(line.strip()) > 0:
            if not q.exec(line):
                raise Exception(traceback.format_exc() + ':\n' + q.lastError().text())
    
    if not q.exec(query.trigger_after_insert):
        raise Exception(traceback.format_exc() + ':\n' + q.lastError().text())
    if not q.exec(query.trigger_after_update):
        raise Exception(traceback.format_exc() + ':\n' + q.lastError().text()) 
    if not q.exec(query.trigger_after_delete):
        raise Exception(traceback.format_exc() + ':\n' + q.lastError().text())


def clear():
    q = QSqlQuery(db)
    if not q.exec(query.clear):
        db.rollback()
        raise Exception(traceback.format_exc() + ':\n' + q.lastError().text())
    else:
        db.commit()

def add_book(file):
    '''
    title, authors, tags, tags_description, series, series_index, lang, translators, description, 
    publish_title, publish_publisher, publish_city, publish_year,
    publish_isbn, publish_series, publish_series_index, 
    type, cover_image, cover_media_type, cover_file_name, file, file_created, file_modified
    '''
    meta = ebookmeta.get_metadata(file)

    q = QSqlQuery(db)
    q.prepare(query.insert_book)
    q.bindValue(0, meta.title)
    q.bindValue(1, meta.author_list_to_string())
    q.bindValue(2, meta.tag_list_to_string())
    q.bindValue(3, meta.tag_description_list_to_string())
    q.bindValue(4, meta.series)
    q.bindValue(5, meta.series_index)
    q.bindValue(6, meta.lang)
    q.bindValue(7, meta.translator_list_to_string())
    q.bindValue(8, meta.description)

    q.bindValue(9, meta.publish_info.title)
    q.bindValue(10, meta.publish_info.publisher)
    q.bindValue(11, meta.publish_info.city)
    q.bindValue(12, meta.publish_info.year)
    q.bindValue(13, meta.publish_info.isbn)
    q.bindValue(14, meta.publish_info.series)
    q.bindValue(15, meta.publish_info.series_index)
    
    q.bindValue(16, meta.format)
    if meta.cover_image_data:
        q.bindValue(17, QByteArray(meta.cover_image_data))
    else:
        q.bindValue(17, None)
    q.bindValue(18, meta.cover_media_type)
    q.bindValue(19, meta.cover_file_name)
    q.bindValue(20, os.path.normpath(meta.file))
    q.bindValue(21, meta.file_created)
    q.bindValue(22, meta.file_modified)
    

    if not q.exec_():
        db.rollback()
        if q.lastError().number() != 19: # Exclude UNIQUE constraint
            raise Exception(traceback.format_exc() + ':\n' + q.lastError().text())
    else:
        db.commit()


def delete_books(list_id):
    q = QSqlQuery(db)
    q.prepare(query.delete_book)

    for id in list_id:
        q.bindValue(0, id)

        if not q.exec_():
            db.rollback()
            raise Exception(traceback.format_exc() + ':\n' + q.lastError().text())
    
    db.commit()

def update_filename(book_id, new_filename):
    q = QSqlQuery(db)
    q.prepare(query.update_filename)
    q.bindValue(0, os.path.normpath(new_filename))
    q.bindValue(1, book_id)
    if not q.exec_():
        db.rollback()
        raise Exception(traceback.format_exc() + ':\n' + q.lastError().text())
    else:
        db.commit()

def update_book_info(book_rec):
    '''
    title, authors, tags, tags_description, series, series_index, lang, translators, description, 
    publish_title, publish_publisher, publish_city, publish_year,
    publish_isbn, publish_series, publish_series_index, 
    type, cover_image, cover_media_type, cover_file_name, file, file_created, file_modified
    '''

    book_id = book_rec.id
    filename = book_rec.file
    try:
        meta = ebookmeta.get_metadata(filename)

        meta.title = book_rec.title
        meta.set_author_list_from_string(book_rec.authors)
        meta.set_tag_list_from_string(book_rec.tags)
        meta.series = book_rec.series
        meta.series_index = book_rec.series_index
        meta.lang = book_rec.lang
        meta.set_translator_list_from_string(book_rec.translators)
        meta.publish_info.title = book_rec.publish_title
        meta.publish_info.publisher = book_rec.publish_publisher
        meta.publish_info.city = book_rec.publish_city
        meta.publish_info.year = book_rec.publish_year
        meta.publish_info.isbn = book_rec.publish_isbn
        meta.publish_info.series = book_rec.publish_series
        meta.publish_info.series_index = book_rec.publish_series_index
        meta.cover_image_data = book_rec.cover_image
        meta.cover_media_type = book_rec.cover_media_type
        meta.cover_file_name = book_rec.cover_file_name
        
        ebookmeta.set_metadata(filename, meta)
        meta = ebookmeta.get_metadata(filename)
    except Exception as e:
        raise Exception(traceback.format_exc())

    q = QSqlQuery(db)
    q.prepare(query.update_book)

    q.bindValue(0, meta.title)
    q.bindValue(1, meta.author_list_to_string())
    q.bindValue(2, meta.tag_list_to_string())
    q.bindValue(3, meta.tag_description_list_to_string())
    q.bindValue(4, meta.series)
    q.bindValue(5, meta.series_index)
    q.bindValue(6, meta.lang)
    q.bindValue(7, meta.translator_list_to_string())
    q.bindValue(8, meta.description)
    
    q.bindValue(9, meta.publish_info.title)
    q.bindValue(10, meta.publish_info.publisher)
    q.bindValue(11, meta.publish_info.city)
    q.bindValue(12, meta.publish_info.year)
    q.bindValue(13, meta.publish_info.isbn)
    q.bindValue(14, meta.publish_info.series)
    q.bindValue(15, meta.publish_info.series_index)
    
    q.bindValue(16, meta.format)
    if meta.cover_image_data:
        q.bindValue(17, QByteArray(meta.cover_image_data))
    else:
        q.bindValue(17, None)
    q.bindValue(18, meta.cover_media_type)
    q.bindValue(19, meta.cover_file_name)

    q.bindValue(20, os.path.normpath(meta.file))
    q.bindValue(21, meta.file_created)
    q.bindValue(22, meta.file_modified)
    
    q.bindValue(23, book_id)

    if not q.exec_():
        db.rollback()
        raise Exception(traceback.format_exc() + ':\n' + q.lastError().text())
    else:
        db.commit()


def get_book_info(book_id):
    '''
    id, title, authors,  tags, tags_description, series, series_index, lang, translators, description, 
    publish_title, publish_publisher, publish_city, publish_year, publish_isbn, publish_series, publish_series_index, 
    cover_image, cover_media_type, cover_file_name, file
    '''
    q = QSqlQuery(db)
    q.prepare(query.select_book)

    book_rec = _get_book_rec()
    q.bindValue(0, book_id)
    if q.exec():
        if q.next():
            book_rec.id = q.value(0)
            book_rec.title = q.value(1)
            book_rec.authors = q.value(2)
            book_rec.tags = q.value(3)
            book_rec.tags_description = q.value(4)
            book_rec.series = q.value(5)
            book_rec.series_index = q.value(6)
            book_rec.lang = q.value(7)
            book_rec.translators = q.value(8)
            book_rec.description = q.value(9)
            
            book_rec.publish_title = q.value(10)
            book_rec.publish_publisher = q.value(11)
            book_rec.publish_city = q.value(12)
            book_rec.publish_year = q.value(13)
            book_rec.publish_isbn = q.value(14)
            book_rec.publish_series = q.value(15)
            book_rec.publish_series_index = q.value(16)

            book_rec.cover_image = q.value(17)
            book_rec.cover_media_type = q.value(18)
            book_rec.cover_file_name = q.value(19)
            book_rec.file = q.value(20)

    else:
        raise Exception(traceback.format_exc() + ':\n' + q.lastError().text())

    return book_rec


def _get_book_rec():
    book_rec = SimpleNamespace(
        id=None, 
        title=None,
        authors=None,
        tags=None,
        tags_description=None,
        series=None,
        series_index=None,
        lang=None,
        translators=None,
        description=None,
        publish_title=None,
        publish_publisher=None,
        publish_city=None,
        publish_year=None,
        publish_isbn=None,
        publish_series=None,
        publish_series_index=None,
        cover_image=None,
        cover_media_type=None,
        cover_file_name=None,
        file=None
    )
    return book_rec
