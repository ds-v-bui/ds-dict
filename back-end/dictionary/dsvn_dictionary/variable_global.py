from pathlib import Path
import os

PATH_FILE = Path(__file__).resolve().parent.parent
# define path and name file excel import
FILE_NAME = os.path.join(PATH_FILE, 'import_ja_text.xlsx')
# define table name to import
TABLE_NAME = 'dsvn_dictionary_ja_dictionary'
# define name of sheet import
SHEET_NAME = 'Sheet1'

# define country language
VIETNAMESE = 'vi'
JAPANESE = 'ja'

# define name file import to translate
FILE_IMPORT = os.path.join(PATH_FILE, 'import_file.txt')
FILE_EXPORT = os.path.join(PATH_FILE, 'export_file.txt')

# define action
READ_FILE = 'r'
WRITE_FILE = 'w'

# define ecoding file
UTF8 = 'utf-8'