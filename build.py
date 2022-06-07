import sys
from argparse import ArgumentParser
from glob import glob
from subprocess import call
import PyInstaller.__main__
import os

# build.py app settings
app_name = 'libro2'
app_icon = {
    'win32': 'src/icon/books.ico'
}
main_module = "src/python/libro2/main.py"
designer_src = 'src/designer'
designer_dest = 'src/python/libro2/ui'
main_dir = os.path.dirname(main_module)
# end of settings 

COMMANDS = {}

def command(f):
    COMMANDS[f.__name__] = f
    return f

def _parse_args():
    parser = ArgumentParser()
    subparser = parser.add_subparsers()
    for name, fn in COMMANDS.items():
        cmd_parser = subparser.add_parser(name, help=fn.__doc__)
        cmd_parser.set_defaults(fn=fn)

    args = parser.parse_args()
    if hasattr(args, 'fn'):
        args.fn()
    else:
        parser.print_help()


@command
def ui():
    '''
    Compile Qt Designer forms to python
    '''
    for f in glob(os.path.join(designer_src, '*.ui')):
        (_, dest_name) = os.path.split(f)
        (dest_name, _) = os.path.splitext(dest_name)
        src = os.path.normpath(f)
        dest = os.path.normpath(os.path.join(designer_dest, dest_name + "_ui.py"))
        print('Compile {0} to {1}'.format(src, dest))
        call('pyuic5 --from-imports {0} -o {1}'.format(src, dest), shell=True)

@command
def rc():
    '''
    Compile QT Designer resources to python
    '''
    for f in glob(os.path.join(designer_src, '*.qrc')):
        (_, dest_name) = os.path.split(f)
        (dest_name, _) = os.path.splitext(dest_name)
        src = os.path.normpath(f)
        dest = os.path.normpath(os.path.join(designer_dest, dest_name + "_rc.py"))
        print('Compile {0} to {1}'.format(src, dest))
        call('pyrcc5  {0} -o {1}'.format(src, dest), shell=True)

@command
def freeze():
    '''
    Compile project to executable
    '''
    platform_app_icon = app_icon[sys.platform]
    print('Compile project to executable')
    PyInstaller.__main__.run([
        '-w',
        '--clean',
        '-y',
        '-n', app_name,
        '--paths', main_dir,
        '-i', platform_app_icon,
        main_module
])


@command
def run():
    '''
    Run project
    '''
    sys.path.append(main_dir)
    app_module = __import__('main')
    app_module.main()
    

if __name__ == '__main__':
    _parse_args()
