
create_tables = '''
    CREATE TABLE books (
            id integer PRIMARY KEY AUTOINCREMENT,
            title text NOT NULL,
            authors text NOT NULL,
            tags text,
            tags_description text, 
            series text,
            series_index int, 
            lang text,
            translators text,
            description text,
            type text NOT NULL,
            cover_image blob,
            cover_media_type text,
            cover_file_name text,
            file text NOT NULL UNIQUE,
            publish_title text,
            publish_publisher text,
            publish_city text,
            publish_year text,
            publish_isbn text,
            publish_series text,
            publish_series_index int,
            file_created text,
            file_modified text   
        );

    CREATE VIEW books_v AS
    SELECT id,
           title,
           authors,
           series,
           series_index,
           tags_description as tags,
           lang,
           translators,
           type, 
           file, 
           file_created as created,
           file_modified as modified
    FROM books;

    CREATE VIRTUAL TABLE book_idx USING fts5 (
        title,
        authors, 
        tags,
        tags_description,
        series,
        lang,
        translators,
        type,
        content = 'books',
        content_rowid = 'id'
    );
'''

trigger_after_insert = '''
    CREATE TRIGGER books_ai AFTER INSERT ON books
    BEGIN
        INSERT INTO book_idx(rowid, title, authors, tags, tags_description, series, lang, translators, type)
            VALUES(new.id, new.title, new.authors, new.tags, new.tags_description, new.series, new.lang, new.translators, new.type);
    END;
'''
trigger_after_delete = '''
    CREATE TRIGGER books_ad AFTER DELETE ON books
    BEGIN
        INSERT INTO book_idx(book_idx, rowid, title, authors, tags, tags_description, series, lang, translators, type)
            VALUES('delete', old.id, old.title, old.authors, old.tags, old.tags_description, old.series, old.lang, old.translators, old.type);
    END;
'''
trigger_after_update = '''
    CREATE TRIGGER books_au AFTER UPDATE ON books
    BEGIN
        INSERT INTO book_idx(book_idx, rowid, title, authors, tags, tags_description, series, lang, translators, type)
            VALUES('delete', old.id, old.title, old.authors, old.tags, old.tags_description, old.series, old.lang, old.translators, old.type);
        INSERT INTO book_idx(rowid, title, authors, tags, tags_description, series, lang, translators, type)
            VALUES(new.id, new.title, new.authors, new.tags, new.tags_description, new.series, new.lang, new.translators, new.type);
    END;
'''


check_db_created = '''
    SELECT count(1) FROM sqlite_master WHERE type="table" AND name="books"
'''


clear = '''
    DELETE FROM books
'''

insert_book = '''
    INSERT INTO books (title, authors, tags, tags_description, series, series_index, 
                      lang, translators, description, 
                      publish_title, publish_publisher, publish_city, publish_year,
                      publish_isbn, publish_series, publish_series_index, 
                      type, cover_image, cover_media_type, 
                      cover_file_name, file, file_created, file_modified)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) 
'''

select_book = '''
    SELECT id, title, authors,  tags, tags_description, series, series_index, lang, 
           translators, description, 
           publish_title, publish_publisher, publish_city, publish_year,
           publish_isbn, publish_series, publish_series_index, 
           type,
           cover_image, cover_media_type, cover_file_name, file
      FROM books
    WHERE id = ?
'''

delete_book = '''
    DELETE FROM books WHERE id = ?
'''

delete_all_books = '''
    DELETE FROM books
'''

update_book = '''
    UPDATE books 
    SET title = ?,
        authors = ?,
        tags = ?,
        tags_description = ?,
        series = ?,
        series_index = ?,
        lang = ?,
        translators = ?,
        description = ?,
        publish_title = ?, 
        publish_publisher = ?,
        publish_city = ?,
        publish_year = ?,
        publish_isbn = ?,
        publish_series = ?,
        publish_series_index = ?,
        type = ?,
        cover_image = ?,
        cover_media_type = ?,
        cover_file_name = ?,
        file = ?, 
        file_created = ?, 
        file_modified = ?
    WHERE id = ?
'''

update_filename = '''
    UPDATE books SET file = ? WHERE id = ?
'''