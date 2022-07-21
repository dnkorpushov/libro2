# ![logo](../master/src/icon/src/Images/bookshelf_32px.png) Libro2

GUI tool for organizing fb2 and epub files.

Key features:
* сhange metadata such as title, author, series, cover, and more
* convert fb2 files to epub, kepub, mobi and awz3. For this feature need [fb2converter](https://github.com/rupor-github/fb2converter)
* rename files by template based on metadata
* support extension plugins
* program runs under Microsoft Windows (10 and above), MacOS (10.14.6 Mojave and above) and Linux.

[User manual (in Russian)](https://github.com/dnkorpushov/libro2/wiki).

## Build Libro2
Requirements: git, python3.9 and above, python modules: pyqt5 (5.12 and above), lxml, pyinstaller, ebookmeta.

Install python and required modules.

Download Libro2:
```
git clone https://github.com/dnkorpushov/libro2.git
cd libro2
```

### For Windows and MacOS
Build executables:
```
python3 build.py freeze 
```
Check dist folder for executables.

Build installer (optional):
```
python3 build.py installer
```
Check intsaller folder for installer. libro2.win32.installer.exe for Windows, libro2.macos.dmg for MacOS.

### For Linux
For Linux run Libro2 from source:
```
./libro2.sh
```

Add libro2 in Application menu for Gnome3 and etc. (optional):
```
python3 build.py install
```

Check Application menu. Tests for Ubuntu 22.04. May not work for other linux distros.

## build.py
Build.py is a script for support libro2 development.
Usage:
```
python3 build.py [command]
```

List of commands:
* run - run project
* ui - compile qt ui forms after change it in qt designer.
* rc - compile rc resorces after change it in qt designer.
* locale - make and compile locale resources. Run command before translating for collect strings for translate. Use qt linguist for translating strings. Run command after translating for compile locale resource files.
* freeze - build executables.
* installer - build installer. Run after freeze command. Use for Windows and MacOS.
* install - add Libro2 icon in Application menu for Linux DE (Gnome3 and etc.)
* clean - clean project (delete unnecessary folder and files, such as build, dist folder and etc.)







