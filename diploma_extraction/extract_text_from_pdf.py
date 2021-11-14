# tika for extracting from pdf
from tika import parser

# pandas to work with csv
import pandas as pd

# os to work with file system
from os import listdir
from os.path import isfile, join

# for passing arguments using terminal
import sys 
try:
    csv_path = sys.argv[1]
except:
    csv_path = "diplomas.csv"

def get_text_from_main_page(filename: str, xml = False) -> str:
    parsed_pdf = parser.from_file(filename, xmlContent = xml)
    data = parsed_pdf['content']
    metadata = parsed_pdf['metadata']
    print(f'\x1B[32mSuccess \x1B[0m- {filename}' if parsed_pdf['status'] == 200 and data else f'\x1B[31mFailed \x1B[0m- {filename} \x1B[31mNO TEXT \x1B[0m')
#     try:
#         data = data.encode('latin-1').decode('CP1251')
#     except:
#         pass
#     data = data[:int(metadata['pdf:charsPerPage'][0])].split('\n')
#     return [line for line in data if line != '']
    return data


# list all files
path = "diploms"
files = []
for folder in listdir(path):
    files += [join(path, folder, file) for file in listdir(join(path, folder)) if isfile(join(path, folder, file))]

# create dataframe
data = pd.DataFrame(columns = ["filename", "text"])

for filename in files:
    try:
        text = get_text_from_main_page(filename)
        data = data.append(pd.Series(
            [filename, text], index = data.columns
        ), ignore_index = True)
#         print(f'\x1B[32mSuccess \x1B[0m- {filename}')
    except Exception as e:
        print(f'\x1B[31mFailed \x1B[0m- {filename}\x1B[31m', e)



data.to_csv(csv_path, index = False)