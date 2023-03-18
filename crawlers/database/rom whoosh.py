import os
import pickle
import PySimpleGUI as sg
from typing import Dict
class Search:
    #Create a search engine

    def __init__(self):
        self.file_index = [] # directory listing returned by os.walk()
        self.results = [] # search results returned from search method
        self.matches = 0 # count of files matched
        self.searched = 0 # count of files searched

    def create_new_index(self, values: Dict[str, str]) -> None:
        #Create a new file index of the root; then save to self.file_index and to pickle file '''
        root_path = values['PATH']
        self.file_index: list = [(root, files) for root, dirs, files in os.walk(root_path) if files]
#if files filters our empty file lists
        # save index to file
        with open('file_index.pkl','wb') as f:
            pickle.dump(self.file_index, f)
    def load_existing_index(self) -> None:
        ''' Load an existing file index into the program '''
        try:
            with open('file_index.pkl','rb') as f:
                self.file_index = pickle.load(f)
        except:
            self.file_index = []

    def search(self, values: Dict[str, str]) -> None:
        ''' Search for the term based on the type in the index; the types of search
            include: contains, startswith, endswith; save the results to file '''
        self.results.clear()#clears the list
        self.matches = 0
        self.searched = 0
        term = values['TERM']
        
        # search for matches and counts results
        for path, files in self.file_index:
            for file in files:
                self.searched +=1
                if (values['CONTAINS'] and term.lower() in file.lower() or 
                    values['STARTSWITH'] and file.lower().startswith(term.lower()) or 
                    values['ENDSWITH'] and file.lower().endswith(term.lower())):

                    result = path.replace('\\','/') + '/' + file
                    #coz backslash are escape characters 
                    self.results.append(result)
                    self.matches +=1
                else:
                    continue 
        # save results to file
        with open('search_results.txt','w') as f:
            for r in self.results:
                f.write(r + '\n')

class interface:
    #Create a GUI
    def __init__(self):
        self.layout: list = [
            [sg.Text('Keyword', size=(12,1)), 
             sg.Input(size=(38,1), focus=True, key="TERM"), 
             sg.Radio('Contains', size=(12,1), group_id='choice', key="CONTAINS", default=True),
             #group_id is just to make sure that all the 3 choices are in the same group so that only 1 can be selected at a time
             sg.Radio('StartsWith', size=(12,1), group_id='choice', key="STARTSWITH"), 
             sg.Radio('EndsWith', size=(12,1), group_id='choice', key="ENDSWITH")],
            [sg.Text('Directory', size=(12,1)), 
             sg.Input('/..', size=(38,1), key="PATH"), 
             #similar to filedialog
             sg.FolderBrowse('Browse', size=(12,1)), 
             sg.Button('New Index', size=(12,1), key="_INDEX_"), 
             sg.Button('Search', size=(12,1), bind_return_key=True, key="_SEARCH_")],
            [sg.Output(size=(200,30))]]
        
        self.window: object = sg.Window('Search Engine', self.layout, element_justification='left')
sg.ChangeLookAndFeel('BluePurple')#can refer other colors too


def main():

    g = interface()
    s = Search()
    s.load_existing_index() # load if exists, otherwise return empty list

    while True:
        click, values = g.window.read()# checks for inputs from user
        if click is None:
            break
        elif click == '_INDEX_':
            s.create_new_index(values)
            print()
            print(">> New index created")
            print()
        elif click == '_SEARCH_':
            s.search(values)

            # print the results to output element
            print()
            for result in s.results:
                print(result)
            
            print()
            print(">> Searched {:,d} files and found {:,d} matches".format(s.searched, s.matches))
            print(">> Results saved in working directory as search_results.txt.")

if __name__ == '__main__':
    print('Starting program...')
    main()   
     
#   https://github.com/israel-dryer/File-Search-Engine/blob/master/file_search_engine.py    
#https://www.youtube.com/watch?v=IWDC9vcBIFQ

