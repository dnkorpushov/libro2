from inspect import ArgSpec
import sys
from argparse import ArgumentParser
from glob import glob
from subprocess import call
import PyInstaller.__main__
import os
import shutil

from importlib_metadata import version

desktop_entry = '''
[Desktop Entry]
Name=Libro2
Version=v1
Icon={0}
X-Icon-Path={1}
Exec={2}
Terminal=false
Type=Application
'''

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
        if name == 'run':
            cmd_parser.add_argument('cmd_args', nargs='*')
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
    del sys.argv[1]
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

    if sys.platform == 'win32':
        call('makensis {0}.nsi'.format(app_name), shell=True)
    
    elif sys.platform == 'darwin':
        src_folder = './dist'
        dest_file = './installer/libro2.macos.dmg'

        if os.path.exists(src_folder):
            shutil.rmtree('./dist/libro2', ignore_errors=True)
            if not os.path.islink('./dist/Applications'):
                os.symlink('/Applications', './dist/Applications')
            if os.path.exists(dest_file):
                os.unlink(dest_file)
            cmd = ['hdiutil', 'create', '-volname', 'libro2', '-format', 'UDZO', '-srcfolder',
                src_folder, dest_file]
            print('Run hdiutil...')
            call(cmd)
        else:
            print(f'Source folder "{src_folder}" not exist. Run freeze before.')


@command
def install():
    if sys.platform == 'linux':
        user_dir = os.path.expanduser('~')
        app_dir = os.path.join(user_dir, '.local/share/applications')
        desktop_file = os.path.join(app_dir,'libro2.desktop')
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        with open(desktop_file, 'w') as f:
            print(sys.argv[0])
            base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            print(base_dir)
            f.write(desktop_entry.format(os.path.join(base_dir, 'linux/libro2.png'),
                                         os.path.join(base_dir, 'linux/'),
                                         os.path.join(base_dir, 'libro2.sh')))
            f.close()
    else:
        print(f'The command is not supported for {sys.platform}')

if __name__ == '__main__':
    _parse_args()
