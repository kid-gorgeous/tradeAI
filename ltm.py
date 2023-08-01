from api import OpenAIClient
from termcolor import colored
import sqlite3

ai = OpenAIClient()

class LongTermMemoryModel:
    def __init__(self):
        self.con = sqlite3.connect('database.db')
        self.c = self.con.cursor()   
        self.connected = False  

    def connect(self):
        self.connected = True

        self.con = sqlite3.connect('database.db')
        self.c = self.con.cursor()    

        print(colored("\nDatabase connected\n", 'green'))

    def disconnect(self):
        self.connected = False
        self.con.commit()
        self.con.close()

        print(colored("\nDropping the table.\n", 'green'))

    def create_table(self):   
        self.c.execute('CREATE TABLE IF NOT EXISTS query(prompt TEXT, completion TEXT)')
        self.con.commit()

    # later may have funny features like temperature, probability, weights or some type of funny business
    def add_completion(self, prompt, completion=''):
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        try:
            if (prompt, completion) == (None, None):
                print("Prompt and completion cannot be empty")

            # in the chance that if a prompt is given with now completion provided  
            # the AI will provide a completion, print an answer, and add it to the
            # database
            if completion == None:
                completion = ai.get_completion(prompt) # this line checks out, and provides an answer
                print(completion)
                cur.execute("INSERT INTO query(prompt,completion) VALUES (?,?)",(prompt, completion))
                con.commit()
            # if a prompt and completion is given, simply add it to the database
            else:
                cur.execute("INSERT INTO query(prompt, completion) VALUES (?,?)",(prompt, completion))
                con.commit()

        except:
            print("Error: No prompt or completion was added to the database.")
            

db = LongTermMemoryModel()
db.connect()
db.add_completion("def add(x, y):")