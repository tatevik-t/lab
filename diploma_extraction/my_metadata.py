import re

def get_metadata(title_page : str) -> tuple:
    if type(title_page) != str or len(title_page) == 0:
        return None, None, None, None, None, None, None, None
    
    year = re.findall(r'(2[0-9]{3})', title_page)
    year = year[-1] if year else None
    
#     people = re.findall(r"([A-Я][а-я]+ [A-Я][а-я]+ [A-Я][а-я]+)|([А-Я]. ?[А-Я]. ?[A-Я][а-я]+)", title_page)
#     print(people)
    
    if re.search(r"(?i)Российско ?- ?армянский", title_page):
        university = 'rau'
        faculty, department, speciality, author, supervisor, title = rau_metadata(title_page)
        
    elif re.search(r"(?i)московский физико[\s\n]?-[\s\n\t]*технический институт", title_page):
        university = 'mipt'
        faculty, department, speciality, author, supervisor, title = mipt_metadata(title_page)
        
    elif re.search(r"(?i)Высшая школа экономики", title_page):
        university = 'hse'
        faculty, department, speciality, author, supervisor, title = hse_metadata(title_page)
        
    elif re.search(r"(?i)дружбы народов", title_page):
        university = 'rudn'
        faculty, department, speciality, author, supervisor, title = rudn_metadata(title_page)
        
    elif (re.search(r"(?i)московский государственный", title_page)):
        university = 'msu'
        faculty, department, speciality, author, supervisor, title = msu_metadata(title_page)
    
    # try to extract something
    else:
        university = re.findall("(?i)$(.*)университет", title_page)
        faculty, department, speciality, author, supervisor, title = any_metadata(title_page)
        
    return year, university, faculty, department, speciality, author, supervisor, title


def splitted_metadata(title_page : str) -> tuple:
    author = None 
    supervisor = None
    title = None
    
    # split in words
    tokenized = re.split(r'\s', title_page)

    for i in range(len(tokenized)):
        if re.match(r"(?i)студент", tokenized[i]) or re.match(r"(?i)исполнитель", tokenized[i]):
            for j in range(i+1, len(tokenized)):
                if tokenized[j] and re.match(r"^[А-Я].*", tokenized[j]) != None:
                    author = tokenized[j]
#                     print("~", author)
                    if tokenized[j+1] and re.match(r"^[А-Я].*", tokenized[j+1]) != None:
                        author += ' ' + tokenized[j+1]
#                         print("~", author)
                        if tokenized[j+2] and re.match(r"^[А-Я].*", tokenized[j+2]) != None:
                            author += ' ' + tokenized[j+2]
#                             print("~", author)
                if author:
                    break
                            
#             print("author:", author)

        if re.match(r"(?i)руководитель", tokenized[i]):
            for j in range(i+1, len(tokenized)):
                if tokenized[j] and re.match(r"^[А-Я].*", tokenized[j]) != None:
                    supervisor = tokenized[j]
#                     print("~", supervisor)
                    if tokenized[j+1] and re.match(r"^[А-Я].*", tokenized[j+1]) != None:
                        supervisor += ' ' + tokenized[j+1]
#                         print("~", supervisor)
                        if tokenized[j+2] and re.match(r"^[А-Я].*", tokenized[j+2]) != None:
                            supervisor += ' ' + tokenized[j+2]
#                             print("~", supervisor)
                if supervisor:
                    break
#             print("supervisor:", supervisor)
            
            
        if re.match(r"(?i)тема", tokenized[i]):
            title = ""
            i += 1
            if(tokenized[i] and tokenized[i][0] in ('"', "«", '“', '“')):
                while(tokenized[i][-1] not in ('"', "»", '”', ".")):
                    title += ' ' + tokenized[i]
                    i += 1
                    while not tokenized[i]:
                        i += 1
#                         print('hm', tokenized[i])
                        
                title += ' ' + tokenized[i]
            else:
                while tokenized[i]:
                    title += ' ' + tokenized[i]
                    i += 1
            title = ' '.join(title.split())
            
#     print(title_page)
    return author, supervisor, title


# RAU
def rau_metadata(title_page : str) -> tuple:
    faculty = "ПМИ"   # as there are no faculty in diploma mentioned
    department = re.findall(r"(?i)Кафедра.*", title_page)
    department = department[0].lower() if department else None
    
    speciality = re.findall(r"(?i)Специальность:\s*(.*)", title_page)
    speciality = speciality[0].lower() if speciality else None
    
    author, supervisor, title = splitted_metadata(title_page)
    
    return faculty, department, speciality, author, supervisor, title


def mipt_metadata(title_page : str) -> tuple:
    faculty = re.findall(r"(?i)Факультет .*", title_page)
    faculty = faculty[0].lower() if faculty else None
        
    department = re.findall(r"(?i)Кафедра.*", title_page)
    department = department[0].lower() if department else None
    
    speciality = re.findall(r"[0-9]{2}.[0-9]{2}.[0-9]{2}", title_page)
    speciality = speciality[0] if speciality else None
    
    author = re.findall(r"C?c?тудент.*(([А-Я]. ?)?[А-Я]. ?[A-Я][а-я]+)|([A-Я][а-я]+ [A-Я][а-я]+ [A-Я][а-я]+)", title_page)
    supervisor = re.findall(r"Научный руководитель.*([А-Я]. ?[А-Я]. [A-Я][а-я]+)", title_page)
    author, supervisor, title = splitted_metadata(title_page)
#     title = re.findall(r"«(.*)»", title_page)
    
    return faculty, department, speciality, author, supervisor, title


def rudn_metadata(title_page : str) -> tuple:
    faculty = re.findall(r"(?i)учебный институт: (.*)", title_page)
    if not faculty:
        faculty = re.findall(r"(?i)\s+(.*)\sинститут", title_page)
    if faculty:
        faculty = faculty[0].lower()
    
    department = re.findall(r"(?i)Кафедра.*", title_page)
    department = department[0] if department else None
    
    speciality = re.findall(r"[0-9]{2}.[0-9]{2}.[0-9]{2}", title_page)
    speciality = speciality[0]  if speciality else None
        
#     author = None
#     supervisor = None
    author, supervisor, title = splitted_metadata(title_page)

    title = re.findall(r"(?i)ТЕМА(.?)", title_page)
    
    return faculty, department, speciality, author, supervisor, title


def hse_metadata(title_page : str) -> tuple:
    faculty = re.findall(r"(?i)Факультет.*", title_page)
    if faculty:
        faculty = faculty[0].lower()
    department = None
    
    speciality = re.findall(r"[0-9]{2}.[0-9]{2}.[0-9]{2}", title_page)
    speciality = speciality[0]  if speciality else None
    
    author, supervisor, title = splitted_metadata(title_page)
    
    return faculty, department, speciality, author, supervisor, title


def msu_metadata(title_page : str) -> tuple:
    faculty = re.findall(r"(?i)\s*(.*Факультет.*)", title_page)
    faculty = faculty[0].lower() if faculty else None
    
    department = re.findall(r"(?i)Кафедра.*", title_page)
    department = department[0].lower() if department else None
    
    speciality = None
    
    author, supervisor, title = splitted_metadata(title_page)
    title = re.findall(r"(?i)Тема:\s*(.*)", title_page)
    
    return faculty, department, speciality, author, supervisor, title


def any_metadata(title_page : str) -> tuple:
    faculty = re.findall(r"(?i)\s*(.*Факультет.*)", title_page)
    faculty = faculty[0].lower() if faculty else None
    
    department = re.findall(r"(?i)Кафедра.*", title_page)
    department = department[0].lower() if department else None
    
    speciality = re.findall(r"[0-9]{2}.[0-9]{2}.[0-9]{2}", title_page)
    speciality = speciality[0]  if speciality else None
    
    author, supervisor, title = splitted_metadata(title_page)

    return faculty, department, speciality, author, supervisor, title
