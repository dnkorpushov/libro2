import os
import ebookmeta
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtCore import QByteArray
import query as query
from types import SimpleNamespace


db_file = os.path.join(os.path.expanduser('~'), 'libro2', 'booklist.db')
db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName(db_file)
db.open()


def init():
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
                print(q.lastError().text())
    
    if not q.exec(query.trigger_after_insert):
        print(q.lastError().text())
    if not q.exec(query.trigger_after_update):
        print(q.lastError().text())
    if not q.exec(query.trigger_after_delete):
        print(q.lastError().text())


def clear():
    q = QSqlQuery(db)
    if not q.exec(query.clear):
        print(q.lastError().text())
        db.rollback()
    else:
        db.commit()

def add_book(file):
    meta = ebookmeta.get_metadata(file)

    q = QSqlQuery(db)
    q.prepare(query.insert_book)
    q.bindValue(0, meta.title)
    q.bindValue(1, meta.get_author_string())
    q.bindValue(2, meta.get_author_sort_string())
    q.bindValue(3, meta.get_tag_string())
    q.bindValue(4, meta.get_tag_description_string())
    q.bindValue(5, meta.series)
    q.bindValue(6, meta.series_index)
    q.bindValue(7, meta.lang)
    q.bindValue(8, meta.get_translator_string())
    q.bindValue(9, meta.description)
    q.bindValue(10, meta.format)
    if meta.cover_image_data:
        q.bindValue(11, QByteArray(meta.cover_image_data))
    else:
        q.bindValue(11, None)
    q.bindValue(12, os.path.normpath(meta.file))

    if not q.exec_():
        db.rollback()
        if q.lastError().number() != 19: # Exclude UNIQUE constraint
            raise Exception(q.lastError().text())
    else:
        db.commit()


def delete_books(list_id):
    q = QSqlQuery(db)
    q.prepare(query.delete_book)

    for id in list_id:
        q.bindValue(0, id)

        if not q.exec_():
            print(q.lastError().text())
            db.rollback()
    
    db.commit()

def update_filename(book_id, new_filename):
    q = QSqlQuery(db)
    q.prepare(query.update_filename)
    q.bindValue(0, os.path.normpath(new_filename))
    q.bindValue(1, book_id)
    if not q.exec_():
        print(q.lastError().text())
        db.rollback()
    else:
        db.commit()

def update_book_info(book_rec):
    book_id = book_rec.id
    filename = book_rec.file

    q = QSqlQuery(db)
    q.prepare(query.update_book)
    q.bindValue(0, book_rec.title)
    q.bindValue(1, book_rec.author)
    q.bindValue(2, book_rec.tags)
    q.bindValue(3, book_rec.series)
    q.bindValue(4, book_rec.series_index)
    q.bindValue(5, book_rec.lang)
    q.bindValue(6, book_rec.translator)
    if book_rec.cover_image:
        q.bindValue(7, QByteArray(book_rec.cover_image))
    else:
        q.bindValue(7, None)
    q.bindValue(8, book_id)
    if not q.exec_():
        print(q.lastError().text())
        db.rollback()
    else:
        db.commit()
        try:
            meta = ebookmeta.get_metadata(filename)

            meta.title = book_rec.title
            meta.set_author_from_string(book_rec.author)
            meta.set_tag_from_string(book_rec.tags)
            meta.series = book_rec.series
            meta.series_index = book_rec.series_index
            meta.lang = book_rec.lang
            meta.set_translator_from_string(book_rec.translator)
            meta.cover_image_data = book_rec.cover_image
            
            ebookmeta.set_metadata(filename, meta)
  
            meta = ebookmeta.get_metadata(filename)
            
            q.prepare(query.update_book_calc_values)
            q.bindValue(0, meta.get_author_sort_string())
            q.bindValue(1, meta.get_tag_description_string())
            q.bindValue(2, book_id)
            if not q.exec_():
                print(q.lastError().text())
                db.rollback()
            else:
                db.commit()
        except Exception as e:
            print(e)


def get_book_info(book_id):
    q = QSqlQuery(db)
    q.prepare(query.select_book)

    book_rec = _get_book_rec()
    q.bindValue(0, book_id)
    if q.exec():
        if q.next():
            book_rec.id = q.value(0)
            book_rec.title = q.value(1)
            book_rec.author = q.value(2)
            book_rec.tags = q.value(3)
            book_rec.tags_description = q.value(4)
            book_rec.series = q.value(5)
            book_rec.series_index = q.value(6)
            book_rec.lang = q.value(7)
            book_rec.translator = q.value(8)
            book_rec.cover_image = q.value(9)
            book_rec.description = q.value(10)
            book_rec.file = q.value(11)

    else:
        print(q.lastError().text())

    return book_rec


def _get_book_rec():
    book_rec = SimpleNamespace(
        id=None, 
        title=None,
        author=None,
        tags=None,
        tags_description=None,
        series=None,
        series_index=None,
        lang=None,
        translator=None,
        cover_image=None,
        decription=None,
        file=None
    )
    return book_rec
