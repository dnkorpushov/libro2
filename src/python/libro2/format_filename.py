import os
import hashlib

def split_ext(path):
    for ext in ['.fb2.zip']:
        if path.lower().endswith(ext):
            return ext
    return os.path.splitext(path)[1]

def path(*args):
    retval = ''
    for arg in args:
        if arg:
            elem = arg
            while elem.endswith('.'):
                elem = elem[:-1]
            if elem:
                retval += elem + '/'  

    return retval


def lst(list, delimiter=', '):
    if len(list) > 0:
        return delimiter.join(list)
    else:
        return ''


def fe(list, suffix=''):
    if len(list) > 0:
        return list[0] + iif(len(list) > 1, suffix)
    else:
        return ''


def iif(cond, if_value, else_value=''):
    if cond:
        return if_value
    else:
        return else_value


def format_person_list(person_list, person_template):
    result = []
    firstname = ''
    middlename = ''
    lastname = ''
    m = ''
    f = ''

    for person in person_list:
        (firstname, middlename, lastname) = get_person_elements(person)
        if middlename:
            m = middlename[0]
        if firstname:
            f = firstname[0]
        result_person = eval(f"f'{person_template}'")
        result.append(result_person.strip())
    return result


def get_person_elements(person):
    firstname = ''
    middlename = ''
    lastname = ''

    person_parts = person.split()
    if len(person_parts) == 3:
        firstname = person_parts[0]
        middlename = person_parts[1]
        lastname = person_parts[2]
    elif len(person_parts) == 2:
        firstname = person_parts[0]
        lastname = person_parts[1]
    else:
        lastname = person
    
    return (replace_symbols(firstname), replace_symbols(middlename), replace_symbols(lastname))

def replace_symbols(s):
    if s:
        for c in '<>:"/\\|?*':
            s = s.replace(c, '_')
    
        return s
    else:
        return ''

def filename_by_template(meta, filename_template, author_template, translator_template):
    title = ''
    authors = []
    author = ''
    translators = []
    translator = ''
    series = ''
    seriesindex = ''
    bookid = ''
    md5 = ''

    if meta.title:
        title = meta.title
    
    if len(meta.author_list) > 0:
        authors = format_person_list(meta.author_list, author_template)
        author = authors[0]
    if len( meta.translator_list) > 0:
        translators = format_person_list(meta.translator_list, translator_template)
        translator = translators[0]

    if meta.series:
        series = meta.series
    if series:
        abbrseries = ''.join(w[0] for w in series.split()) 
    if meta.series_index:
        seriesindex = str(meta.series_index)
    
    if meta.identifier:
        bookid = meta.identifier
    md5 = ''
    with open(meta.file, 'rb') as f:
        data = f.read()
        md5 = hashlib.md5(data).hexdigest()

    title = replace_symbols(title)
    author = replace_symbols(author)
    translator = replace_symbols(translator)
    series = replace_symbols(series)
    bookid = replace_symbols(bookid)
    md5 = replace_symbols(md5)
    
    result = eval(f"f'{filename_template}'")
    file_ext = split_ext(meta.file)
    result = result.strip() + file_ext

    return os.path.normpath(result) 

