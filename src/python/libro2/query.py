
create_tables = '''
    CREATE TABLE book (
            id integer PRIMARY KEY AUTOINCREMENT,
            title text NOT NULL,
            author text NOT NULL,
            author_sort text, 
            tags text,
            tags_description text, 
            series text,
            series_index int, 
            lang text,
            translator text,
            description text,
            type text NOT NULL,
            cover_image blob,
            file text NOT NULL UNIQUE
        );

    CREATE VIEW book_v AS
    SELECT id,
           title,
           author_sort as author,
           series,
           series_index,
           tags_description as tags,
           lang,
           translator,
           type, 
           file
    FROM book;

    CREATE VIRTUAL TABLE book_idx USING fts5 (
        title,
        author, 
        tags,
        tags_description,
        series,
        lang,
        translator,
        type,
        content = 'book',
        content_rowid = 'id'
    );
'''

trigger_after_insert = '''
    CREATE TRIGGER book_ai AFTER INSERT ON book
    BEGIN
        INSERT INTO book_idx(rowid, title, author, tags, tags_description, series, lang, translator, type)
            VALUES(new.id, new.title, new.author, new.tags, new.tags_description, new.series, new.lang, new.translator, new.type);
    END;
'''
trigger_after_delete = '''
    CREATE TRIGGER book_ad AFTER DELETE ON book
    BEGIN
        INSERT INTO book_idx(book_idx, rowid, title, author, tags, tags_description, series, lang, translator, type)
            VALUES('delete', old.id, old.title, old.author, old.tags, old.tags_description, old.series, old.lang, old.translator, old.type);
    END;
'''
trigger_after_update = '''
    CREATE TRIGGER book_au AFTER UPDATE ON book
    BEGIN
        INSERT INTO book_idx(book_idx, rowid, title, author, tags, tags_description, series, lang, translator, type)
            VALUES('delete', old.id, old.title, old.author, old.tags, old.tags_description, old.series, old.lang, old.translator, old.type);
        INSERT INTO book_idx(rowid, title, author, tags, tags_description, series, lang, translator, type)
            VALUES(new.id, new.title, new.author, new.tags, new.tags_description, new.series, new.lang, new.translator, new.type);
    END;
'''


check_db_created = '''
    SELECT count(1) FROM sqlite_master WHERE type="table" AND name="book"
'''


clear = '''
    DELETE FROM book
'''

insert_book = '''
    INSERT INTO book (title, author, author_sort, tags, tags_description, series, series_index, lang, translator, description, type, cover_image, file)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) 
'''

select_book = '''
    SELECT id, title, author,  tags, tags_description, series, series_index, lang, translator, cover_image, description, file
      FROM book
    WHERE id = ?
'''

delete_book = '''
    DELETE FROM book WHERE id = ?
'''

update_book = '''
    UPDATE book 
    SET title = ?,
        author = ?,
        tags = ?,
        series = ?,
        series_index = ?,
        lang = ?,
        translator = ?,
        cover_image = ?
    WHERE id = ?
'''

update_book_calc_values = '''
    UPDATE book
    SET author_sort = ?,
        tags_description = ?
    WHERE id = ?
'''