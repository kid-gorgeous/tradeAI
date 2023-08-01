""" 

    This menu is a work in progress; for right now it will only display information
    from the symbol CSV files. It will display the following information: Date, Open,
    High, Low, Close, Adj Close, Volume.

    The menu will allow the user to search from a directory of symbols downloaded from 
    the S&P 500. The user will be able to search for a symbol and the menu will display
    the information from the CSV file for that symbol. It will also display the sentiment
    analysis for that symbol. 



"""

import csv
import pandas
import termcolor

class Menu:
    # Simply name the file to search
    def __init__(self, filename):
        self.filename = filename

    # Working
    def openfile(self):
        filename = self.filename
        with open(f'symbols/{filename}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                print(', '.join(row))

    # From here I want to grab the Head of the stack of the CSV file and display it
    #   or to prepare the information to be displayed in a JSON format in order to send and receive
    #   data from the "server".
    
while True:
    inp = input("\nEnter a symbol: ")
    menu = Menu(inp)
    menu.openfile()