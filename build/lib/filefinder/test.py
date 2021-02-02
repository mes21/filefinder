

import os
import datetime
from datetime import datetime as dt

def ext_filter(check_str, matchlist, exclude=False):

    # add "." if missing
    checks_list_ = []
    for ext in matchlist:
        if isinstance(ext, str):
            if ext[0] != ".":
                checks_list_.append("." + ext)
            else:
                checks_list_.append(ext)

    if exclude is False:
        for check in checks_list_:
            print(check_str)
            if check == check_str:
                return True
        return False

    else:
        for check in checks_list_:
            print(check_str)
            if check == check_str:
                return False
        return True

def or_filter(check_str, matchlist, exclude=False):

    if exclude is False:
        for check in matchlist:
            print(check_str)
            if check in check_str:
                return False
        return True

    else:
        for check in matchlist:
            print(check_str)
            if check in check_str:
                return True
        return False

def and_filter(check_str, matchlist, exclude=False):

    if exclude is False:
        for check in matchlist:
            print(check_str)
            if check not in check_str:
                return False
        return True

    else:
        for check in matchlist:
            print(check_str)
            if check in check_str:
                return False
        return True

def date_filter(check_file, date, date_pattern="%Y%m%d", os_date=True,  , exclude=False)


    if isinstance(date, str):
        date = dt.strptime(date, date_pattern)

    elif isinstance(date, datetime.date):


    elif:
        return False



if __name__ == "__main__":
    
    path = r"C:\temp"
    raw_list = []
    for root, dirs, files in os.walk(path):
        for name in files:
            raw_list.append(os.path.join(root, name))
        for name in dirs:
            if os.path.isfile(os.path.join(root, name)):
                raw_list.append(os.path.join(root, name))


    # ext
    raw_list = [x for x in raw_list if ext_filter(os.path.splitext(x)[1],[".csv", ".zip", ".html", ".py"],True)]

    print(raw_list)

    # path
    # or
    #raw_list = [x for x in raw_list if or_filter(os.path.split(x)[0],["01_Python", "aws_merge"],True)]
    # and
    raw_list = [x for x in raw_list if and_filter(os.path.split(x)[0],["temp", "aws_merge"],False)]
    
    
    
    
    
    print(raw_list)