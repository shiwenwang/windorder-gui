# -*- mode: python -*-

block_cipher = None


a = Analysis(['gui\\main.py'],
             pathex=['E:\\WorkSpace\\6_Programming\\wind-order-gui\\gui'],
             binaries=[],
             datas=[],
             hiddenimports=['mysql','mysql.connector.locales.eng.client_error'],
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
