### TradeAI - ChatGPT, and Machine Learning enhanced Portfolio Management System

> *"Trade like you've never traded before ... misrepresented, and under-educated"* - Me ...

#### File information:
    - api.py will provide the user access to the OpenAI API
    - cli.py will grant them the ability to chat via command line arguements
    - menu.py will display *most* of the infromation provided
    - risk_mgmt.py provides risk information on the portfolio
    - screener.py provides measured market data, and downloads it for later
    - sentiment_analysis.py provides a measured evaluation of the value of that daily market news
    - macroeco.py will identify any macroeconomic changes of the global enviroment
    - spa.py will become a single page application to view information and to visualize data

#### Setup CLI:
    - Add your OpenAI API key if so desired
    - Install the requirements
    - Update the API key in the api.py file
    - Alias repl to engage with OpenAI
    - Converse with ChatGPT 3.5
    - Run/Modify menu.py for TA tasks


#### Web Features:
    - Symbol Screener (S&P500 index, ~500 symbols: 30% of best performers) 
    - Sentiment Analysizer (Mean Sentiment, and Conformal information)
    - Risk Analysizer (The daredevils tool belt)
    - Streamlit provided Webframework (deployed on HerokU! via trade.ejdev.com!)
    - A very archaic News Table (but always upto date)
    - (WIP) Voice Transcriber...? (whisper openai or something)
    - (WIP) Full-Stack Application features.... (Flask???, Streamlit???)
    - (WIP) CLI, and REST API interface (fastapi???, click???, sys.argv???)

#### Usage and TODOs:
    - Improving on overall modility of the application. (Toot toot)
    - Most python files are not encapsulated yet (Oh but they will be...)
    - The menu, and overall functionality of the application needs to be reanalysized on ease of use (CMD removed, move to APP)
    - The front end of the application needs work (YEAH! STYLE EVERYTHING!)
    - Requirements must be documented (No )
    - Configurations must be written (Just started lol)
    - Modules must be named, and updated (This is mostly done)
    - Reincorperating an OpenAI wrapper for better queries and prediction models
    - Virtualization in a container or within a virtual enviorment (venv)

---
### A brief introduction: 

In addition to the CLI interface, and menu systems, I will be working to provide a LTM module on top of the OpenAI provide API. For my convenience I've intentionally built onto a AI framework. Currently Im working on gathering data for my experiments. Consequently, I've taken this upon myself, and has become work in itself. Luckily I am gather market information with a baked in REST API.

Information like sentiment scores, news, risk, and popularity are gathered, and measured before being transformed into an OpenAI embedding. Once an embedding is created its is used to finetune a customized OpenAI chat model that will allow the user to converse with the trading information provided. 

Further features will allow for better data scrapping methods, and will allow the user to browse the internet will chatting with the Bot about the current symbol, new, or query that the user is looking for while also learning more about the user themselves and gathering data itself. 

### On the horizon

Even though this system is designed to allow the user to view and maintain a large
field of information on all of the symbols provided by the S&P500, it will not act 
on its own free will and execute trades. It will allow the user to gather, and view data at their free will. The machine learning capabilites that are build into these modules will allow the user to run a variety of different methods of applications to follow. Documentation is a work in progress but will be updated to provide a indepth explaination of these features

For my own personal benifit and for the sake of research intend to employed an indication system, and a personalize autonomous trading system that will help leverage risk and value in real time in the case of unique market conditions.

It will aggregate information from a variety of sources like youtube, twitter(maybe), yahoo finance, and other places that will provide valuable data, and information that can be scrubbed and prepared to align training models.

It would be nice to provide a system that will help the user trade on the NYSE based on the information provide by the S&P500, but such is the case of a lack of
trustworthy ways to access brokrage accounts... Alas, it is on the TODO list.

Further information will be provided. Stay tuned!

It might be time ... {prompt}, 

### Push to the Press: August 18th, 2023
Okay so update... we're working on the prompt DataType... It will work soon enough.
Anyways, we're out here adding a Longterm Shortterm Memory "system" to this mess. I'm tired of thinking about this Economy Drama so I'm just going to let the computer handle it, ya dig? So, that's what this next update will be about. I'll put a number to it, and read up on what an 'Alpha' is and add a version number to everythin'.

Btw, this will not make you ***rich*** but maybe it'll make you *wealthy*

#### On the grill: August 29th, 2023
Back again, and of course not much has been accomplished. I'm focusing on optimizing the machine learning features that are implemented and the future tendencies that I would like to incorporate into the over all functionality of this application. I'm imagining a way to communicate with a finetuned financial model. I'm hoping to learning more about financing as a whole throughout lifecycle of my application. I'm attending school again and finishing up my senior year of college but I intend to try and add new features weekly or bi-weekly. We'll see. 

> Off to school.

#### From the otherside of the looking glass, October 2nd, 2023
After taking a step back, I've planned to structurize this application. It features capabilities that I have lost sight off. I am refocusing 
development on functionality and learning potential. The chat features are okay, but they are not bounded by the intelligent databases that provide
resources for scripts, and utilities. I would like to feature my own regression models and a model handler that will allow me to change or tweek the
learning abilites of a machine learning algorithm. 

##### Sidebar update: I started a new project. It's being graded at school.
So basically, I'm watching you. If you cheat, we know. If you submit a paper that's plagerized.. We'll know. 
... If you forgot to brush your teeth, they'll jknow. 

This project is not of your attention....... But, you'll have ours. This team based project is a anti-cheat software.
It will feature: 
    - Facial Recognition
    - Patterned Behavioral Modelling
    - Timers and Sensors
    - Bells and Whistles
    - A client based server streaming service

But, I gotta ask the rest of the team how ambition they are feeling. I want office space, but we'll see.


#### Directory Tree:
- env
- utils
    - federal reserve ap
    - openapi (for chat capabilities)
- scripts
- misc. files

##### Citations:
 - https://site.financialmodelingprep.com/developer/docs/

---
##### MIT License
Copywrite 2023, Evan Julius

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.