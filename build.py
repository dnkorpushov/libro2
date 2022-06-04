import PyInstaller.__main__
import os

app_name = 'libro2'
app_icon = 'src/icon/books.ico'
main_module = "src/python/libro2/main.py"

main_dir = os.path.dirname(main_module)



PyInstaller.__main__.run([
    '-w',
    '--clean',
    '-y',
    '-n', app_name,
    '--paths', main_dir,
    '-i',app_icon,
    main_module
])