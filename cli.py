from api import OpenAIClient, openai
# from ltm import LongTermMemoryModel
from termcolor import colored

# --------------------------------------------------------------------------------- #
ai = OpenAIClient()
# db = LongTermMemoryModel()

import sys

# --------------------------------------------------------------------------------- #

class aiCLI:
    def __init__(self):
        self.api_key = ai.api_key
        self.max_tokens = ai.max_tokens
        self.temperature = ai.temperature

    


if __name__ == "__main__":
    if sys.argv[1] == "--comp":
        ai.get_completion(sys.argv[2])
    if sys.argv[1] == "--code":
        ai.code_completion(sys.argv[2])
    if sys.argv[1] == "--img":
        ai.get_image(sys.argv[2])
    if sys.argv[1] == "--repl":
        print("Thank you for using Vitural Box 3000. It can be used to generate search queries, code, and images. With visual embeddings, it can rip your arm off. It will literally haunt your dreams. Do not use this product its definitely not safe. \n")
        print("A basic requeast from black box 3000 will provide visual embeddings of the prompt upon user request. Upon auditorial request it may provide a response generatered from a LLaMa model. This is were things got really tricky. This will probably end the world,,, \n but its whatever.\n\n")
            
        while True:
            prompt = input(colored("\n>>> ", "green"))
            if prompt == "exit":
                break
            else:
                openai.api_key = ai.api_key
                response = openai.Completion.create(
                    model = "text-davinci-003",
                    prompt = prompt,
                    max_tokens = ai.max_tokens,
                    temperature = ai.temperature,
                )
                completion = response['choices'][0]['text']
                print(colored(completion, 'green'))
                # db.add_completion(prompt, completion)
            print("\nEnter prompt or type 'exit' to exit")

        
        # repl stands for read-eval-print-loop and will go here to connect to ltm and api without concurrency issues
        pass

    # Change model (but is unoperationnal)
    if sys.argv[1] == "--change-mode":
        try:
            if sys.argv[1] == "--change-mode" and sys.argv[2] == "--list-modes":
                argv = "--list-modes"
                ai.changeModel(argv)
            if sys.argv[1] == "--change-mode" and sys.argv[2] == "--length":
                argv = "--length"
                ai.changeModel(argv)
            else:
                ai.changeModel()
        except:
            print("You must append a callee to the calling argument --change-mode ")
            pass

    if sys.argv[1] == "--help":
        try:
            if sys.argv[1] == "--help" and sys.argv[2] == "--comp":
                print("This will allow the user to call a single prompt and completion")
                print("You may not change the model without a role.\n")
            if sys.argv[1] == "--help" and sys.argv[2] == "--code":
                print("This will allow the user to call a single prompt and completion and output only the code snippet")
                print("You may not change the model without a role.\n")
            if sys.argv[1] == "--help" and sys.argv[2] == "--img":
                print("This will allow the user to call a single prompt and completion and output only the image")
                print("You may not change the model without a role.\n")
            if sys.argv[1] == "--help" and sys.argv[2] == "--repl":
                print("This will allow the user to call upon a REPL to use the API")
                print("You may not change the model without a role.\n")
            if sys.argv[1] == "--help" and sys.argv[2] == "--change-mode":
                print("This will allow the user to call a verity of arguments to change the model")
                print("Available arguments: --list-modes, --length")
                print("You may not change the model without the correct role.\n")

            if sys.argv[1] == "--help" and sys.argv[2] == "--database":
                print("This will allow the user to call a verity of arguments to change the model")
                print("Available arguments: --create")
                print("You may not change the model without the correct role.\n")
        except:
            print("Available arguments: --comp, --code, --img, --repl, --change-mode, --database\n")
        
    if sys.argv[1] == "--ltm":
        pass