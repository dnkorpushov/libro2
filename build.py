import sys
from argparse import ArgumentParser
from glob import glob
from subprocess import call
import PyInstaller.__main__
import os
import shutil

# build.py app settings
app_name = 'libro2'
app_icon = {
    'win32': 'src/icon/libro2.ico',
    'darwin': 'src/icon/libro2.icns'
}
main_module = "src/python/libro2/main.py"
designer_src = 'src/designer'
designer_dest = 'src/python/libro2/ui'

locale_src = 'src/locale'
locale_dest = 'src/python/libro2/locale'

add_data = {
    'src/python/libro2/locale': 'locale'
}

main_dir = os.path.dirname(main_module)
# end of settings 

COMMANDS = {}

# Set working dir
os.chdir(sys.path[0]) 

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
def locale():
    '''
    Compile QT locale resources
    '''
    for pro in glob('*.pro'):
        call('pylupdate5 -translate-function _t {0}'.format(pro), shell=True)

    for ts in glob(os.path.join(locale_src, '*.ts')):
        dst = os.path.join(locale_dest, os.path.splitext(os.path.split(ts)[1])[0] + '.qm')
        call('lrelease {0} -qm {1}'.format(ts, dst), shell=True)

@command
def freeze():
    '''
    Compile project to executable
    '''
    platform_app_icon = app_icon[sys.platform]
    print('Compile project to executable')

    args = [
        '-w',
        '--clean',
        '-y',
        '-n', app_name,
        '--paths', main_dir,
        '-i', platform_app_icon
    ]

    for k in add_data:
        args.append('--add-data')
        args.append(k + os.pathsep + add_data[k])
    args.append(main_module)

    PyInstaller.__main__.run(args)


@command
def run():
    '''
    Run project
    '''
    sys.path.append(main_dir)
    app_module = __import__('main')
    app_module.main()
    
@command 
def clean():
    '''
    Clean project
    '''
    shutil.rmtree('.qt_for_python', ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('installer', ignore_errors=True)
    for spec in glob('*.spec'):
        os.remove(spec)

@command
def installer():
    '''
    Make installer for app
    '''
    
    if not os.path.exists('installer'):
        os.makedirs('installer')

    call('makensis {0}.nsi'.format(app_name), shell=True)

if __name__ == '__main__':
    _parse_args()
