### 利用PyInstaller打包#### 方法一在根目录执行（建议在虚拟环境中，可使exe较小）：```pyinstaller WindOrder.spec```#### 方法二- 启动时没有控制台：```pyinstaller -w -n=WindOrder -i=windorder.ico gui/main.py```- 启动时有控制台(方便调试)：```pyinstaller -n=WindOrder -i=windorder.ico gui/main.py```