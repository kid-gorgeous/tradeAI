# from ltm import DatabaseModel
from termcolor import colored
import requests
import openai
import sys


class OpenAIClient:
    def __init__(self):
        self.api_key = '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'
        self.max_tokens = 1000
        self.temperature = 0.5
        

        # self.db = DatabaseModel().create_table()
  
    def get_completion(self, prompt, quant=None):
        openai.api_key = self.api_key
        response = openai.Completion.create(
            model = "text-davinci-003",
            prompt = prompt,
            max_tokens = self.max_tokens,
            temperature = self.temperature,
        )
        print(colored(response['choices'][0]['text'], 'green'))
        return response['choices'][0]['text']

    def code_completion(self, prompt):
        openai.api_key = self.api_key
        response = openai.Completion.create(
            model = "text-davinci-003",
            prompt = prompt,
            max_tokens = self.max_tokens,
            temperature = self.temperature,
        )
        print(prompt)
        return print(colored(response['choices'][0]['text'], 'green'))

    def get_image(self, prompt):
        
        openai.api_key = self.api_key
        response = openai.Image.create(
            prompt = prompt,
            n = 2,
            size = "1024x1024",
        )


        print("\n> Ctrl + Click to open image in new tab")
        return(print(response['data'][0]['url']))

    def changeModel(self, argv=None, argv2=None):
        openai.api_key = self.api_key

        # OpenAI API provides lists of models
        lists = openai.Model.list()

        # if no arguments are given allow the compiler to pass
        if(argv == None):
            pass

        # if the --help argument is given, print the help menu
        if(argv == '--help'):
            print("This will allow the user to call a verity of arguments to change the model")
            print("Available arguments: --list-modes, --length")
            print("\nYou may not change the model without the correct role.")

        if(argv == '--list-modes'):
            for i in range(len(lists['data'])):
                print("Available model at index", i, ": ", lists['data'][i]['id'])

        if(argv == '--length'):
            print("There are ", len(lists['data']), "models available")

        print(lists)
            
