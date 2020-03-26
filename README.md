### 利用PyInstaller打包
#### 1. 在根目录执行（建议在虚拟环境中, .exe更小)
- 启动时没有控制台：

```
pyinstaller -w -n=windorder-v<version> -i=res/img/windorder.ico gui/main.py
```

- 启动时有控制台(方便调试)：

```
pyinstaller -n=windorder-v<version> -i=res/img/windorder.ico gui/main.py
```

根目录将生成 `windorder-v<version>.spec` 文件
```python
# -*- mode: python -*-

block_cipher = None


a = Analysis(['gui\\main.py'],
             pathex=['E:\\WorkSpace\\6_Programming\\wind-order-gui'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='windorder-v1.2.3',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='windorder.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='windorder-v1.2.3')

```

#### 2. 修改`windorder-v<version>.spec` 文件
```python
pathex=['E:\\WorkSpace\\6_Programming\\wind-order-gui\gui'],
hiddenimports=['mysql','mysql.connector.locales.eng.client_error'],
```

#### 3. 最终执行
`pyinstaller windorder-v<version>.spec`

可执行程序在`dist/windorder-v<version>`文件夹中。
