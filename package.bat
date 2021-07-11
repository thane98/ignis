pyinstaller -F -n ignis -i ignis.ico ignis\controllers\main.py
copy ignis.ico dist
copy LICENSE.txt dist
copy ignis-fe14.yml dist
xcopy Data dist\Data\ /s /e /y
xcopy venv\Lib\site-packages\PySide6\plugins\platforms dist\platforms\ /s /e /y
