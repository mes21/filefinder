import os

import time
import concurrent.futures

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
            print(check, check_str)
            if check == check_str:
                return True
        return False

    else:
        for check in checks_list_:
            if check == check_str:
                return False
        return True

def or_filter(check_str, matchlist, exclude=False):

    if exclude is False:
        for check in matchlist:
            if check in check_str:
                return False
        return True

    else:
        for check in matchlist:
            if check in check_str:
                return True
        return False

def and_filter(check_str, matchlist, exclude=False):

    if exclude is False:
        for check in matchlist:
            if check not in check_str:
                return False
        return True

    else:
        for check in matchlist:
            if check in check_str:
                return False
        return True

def strtolist(input_):
    if isinstance(input_, str):
        return [input_]
    else:
        return input_

def maxsize_filter(file_, size, exclude=False):

    if exclude is False:
        if os.path.getsize(file_)/1000000 < size:
            return True
        else:
            return False
    else:
        if os.path.getsize(file_)/1000000 < size:
            return False
        else:
            return True

def minsize_filter(file_, size, exclude=False):

    if exclude is False:
        if os.path.getsize(file_)/1000000 > size:
            return True
        else:
            return False
    else:
        if os.path.getsize(file_)/1000000 > size:
            return False
        else:
            return True            

class FileFinder():
    def __init__(self, path, local=True, zip=False, bucket=None, aws_cred=None):

        #print(path)
        #print(os.listdir(path))
        
        self.raw_list = []
        self.match_list = []

        dir_list = []
        if bucket is None:
            if local is True:
                for root, dirs, files in os.walk(path):
                    for name in files:
                        self.raw_list.append(os.path.join(root, name))
                    for name in dirs:
                        if os.path.isfile(os.path.join(root, name)):
                            self.raw_list.append(os.path.join(root, name))

            # use threading for network drives
            else:

                self.__list(path)
        
        # get list of AWS Bucket
        else:
            pass


        self.match_list = self.raw_list.copy()

    def __list(self, path):

        dir_list = []
        for el in os.listdir(path):
            el_ = os.path.join(path, el)
            if os.path.isdir(el_) is True:
                dir_list.append(el_)
            else:
                self.raw_list.append(el_)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:

            results = executor.map(self.__list, dir_list)
            #for res in results:
            #    pass




    def namefilter(self, path_and=None, path_or=None, file_and=None, file_or=None, file_ext=None, exclude=False):

        if file_ext:
            self.match_list = [x for x in self.match_list if ext_filter(os.path.splitext(x)[1], strtolist(file_ext), exclude)]

        if path_or:
            self.match_list = [x for x in self.match_list if or_filter(os.path.split(x)[0], strtolist(path_or), exclude)]

        if path_and:
            self.match_list = [x for x in self.match_list if and_filter(os.path.split(x)[0], strtolist(path_and), exclude)]

        if file_or:
            self.match_list = [x for x in self.match_list if or_filter(os.path.split(x)[1], strtolist(file_or), exclude)]

        if file_and:
            self.match_list = [x for x in self.match_list if and_filter(os.path.split(x)[1], strtolist(file_and), exclude)]


    def sizefilter(self, maxsize=None, minsize=None, exclude=False):
        
        if maxsize:
            self.match_list = [x for x in self.match_list if maxsize_filter(x, maxsize, exclude)]

        if minsize:
            self.match_list = [x for x in self.match_list if minsize_filter(x, maxsize, exclude)]


    def datefilter(self, date_older, date_newer, date_match, pattern_date="%Y%m%d", os_date=None, exclude=False):
          
        if os_date:


    def resetfilter(self):
        self.match_list = self.raw_list.copy()


    def result(self):
        return self.match_list


if __name__ == '__main__':

    
    test_path = r"C:\temp"
    t1 = time.time()


    


    f = FileFinder(test_path, local=False)
    f.namefilter(file_ext="zip", exclude=False)
    res = f.result()
    print(len(res))
    print("res:", res)
    
    t2 = time.time()

    print(t2-t1)





    raw_list = []

    t1 = time.time()
    for root, dirs, files in os.walk(test_path):
        for name in files:
            raw_list.append(os.path.join(root, name))
        for name in dirs:
            if os.path.isfile(os.path.join(root, name)):
                raw_list.append(os.path.join(root, name))

    t2 = time.time()
    print(len(raw_list))
    print(t2-t1)