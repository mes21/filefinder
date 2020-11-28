import os

import time
import concurrent.futures







class FileFinder():
    def __init__(self, path, local=True, zip=False):

        #print(path)
        #print(os.listdir(path))
        
        self.raw_list = []
        self.match_list = []

        dir_list = []
        
        if local is True:
            for root, dirs, files in os.walk(test_path):
                for name in files:
                    raw_list.append(os.path.join(root, name))
                for name in dirs:
                    if os.path.isfile(os.path.join(root, name)):
                        raw_list.append(os.path.join(root, name))

        # use threading for network drives
        else:

            for el in os.listdir(path):
                el_ = os.path.join(path, el)
                
                #print("el:", el_)
                if os.path.isdir(el_) is True:
                    dir_list.append(el_)
                else:
                    self.raw_list.append(el_)

            with concurrent.futures.ThreadPoolExecutor() as executor:

                results = executor.map(self.__list, dir_list)
                #for res in results:
                #    pass

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

    def __getchecklist(self):

        if len(self.match_list) == 0:
            return self.raw_list
        else:
            return self.match_list

    def __strtolist(self, input_):
        if isinstance(input_, str):
            return [input_]
        else:
            return input_


    def __updatechecklist(self, checklist_, match_list, match):

        if match is True:
            return match_list
               
        else:
            for el in match_list:
                if el in checklist_:
                    checklist_.remove(el)
 
            return checklist_


    def namefilter(self, path_and=None, path_or=None, file_and=None, file_or=None, file_ext=None, match=True):

        new_match_list = []

        check_list = self.__getchecklist()

        if file_ext is not None:
            match_list = []
            ext_list = self.__strtolist(file_ext)
            checks_list_ = []
            # add "." if missing
            for ext in ext_list:
                if isinstance(ext, str):
                    if ext[0] != ".":
                        checks_list_.append("." + ext)
                    else:
                        checks_list_.append(ext)

            # check for matches
            for file_ in check_list:
                file_ext = os.path.splitext(file_)[1]
                
                if file_ext in checks_list_:
                    match_list.append(file_)

        check_list = self.__updatechecklist(check_list, match_list, match)
        print("check_list", check_list)
        self.match_list = check_list



    def sizefilter(self, maxsize=None, minsize=None):
        pass

    def datefilter(self, date, operator):
        pass

    def result(self):
        return self.match_list


if __name__ == '__main__':

    
    test_path = r"C:\temp"
    t1 = time.time()


    


    f = FileFinder(test_path, local=False)
    print("RES:")
    f.namefilter(file_ext="zip", match=False)
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