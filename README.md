# AI-Report-Assistant
🛸 Harness the Power of AI for all your reporting needs 🚀

Kind of, it works but whether it is of use to you is a different matter.

***Not a real API Key*** 😎
![image](https://user-images.githubusercontent.com/130473605/232334604-70469370-682c-4c4f-9e69-7faafc1c439c.png)


Mainly came about as I wanted to generate a decent Knowledge Base for reporting and trying to save time when Googling for issues as not to use Nessus Writeups.

Like everything I ever do, it goes from an idea to spending more time than I should trying to get it to work.

## Is it glorified google?

Basically yes, you could easily get all the information it returns by either a) googling for the information or b) going to chatgpt and asking it questions. 

But......command line tools are much cooler imo. 

## So what is it?

Its just a Python scipt for interacting with the chatgpt api. 
* Uses the gpt-3.5-turbo model. 
* Temperature is set to 0.5 (see https://www.atmosera.com/ai/understanding-chatgpt/)
* Only dependency is `openai`

`pip install openai`

## You need an openAI API Key

Sign into chatgpt and get an API Key - You get $5 free. It costs about $0.002 per API request so free credit will probably expire before you use up that amount.

## Is it well built?

Doubtful, I have minimal developer experience. This was done to serve a purpose and to improve my python understanding. If you have any issues with the code feel free to re-write it.

## Is it well tested?

Works on my kali VM 🤷🏼‍♂️

## TODO

Needs more error handling and colours, everyone likes a coloured output. Possibly add some extra parameters to use for the writeups as currently it just uses the pluginName from the .nessus xml file. 

# How to use

You can use it interactively to get writeups for a single issue or pass it a .nessus file and it will parse it, pulling all Critical, High, Medium and Low Issues then using the pluginName as input to get writeups. 

All issues are then saved in an .txt file.


Run with `python3 Report-Assist.py`

## Can it be tweaked?

100% - See below. This is sent with every request, it tells chatgpt what is expected. 

```python
# Initialize message history
message_history = [
    {"role": "user", "content": "You are a penetration test report writing technical assistant. "
                                 "Give me Penetration Test Report writeups for each vulnerability I give you. "
                                 "Provide a Description, Background, Risk, Impact and remediaton section. "
                                 "All respsonses must be highly technical in nature. show the commands "
                                 "used to check for this issue."}]
```

## Nessus File
If passing a nessus file choose option 2 and give it the filename.

![image](https://user-images.githubusercontent.com/130473605/232334859-9b71c4fd-e0db-4b43-89ca-1c4d5b456439.png)


Will output .txt file with Issues in Current Directory

![image](https://user-images.githubusercontent.com/130473605/232334883-94223cd6-0b96-40ea-8925-ebe1e9eb1fe8.png)


## Interactive Mode

Try to be specific for best results. If choosing option 1 just give it the issue ie `>: SMB Signing enabled but not required on Windows 10 host` 

![image](https://user-images.githubusercontent.com/130473605/232335023-3c5a3f03-43b3-4359-a9e5-4dd9a91ca8d6.png)


Return to Menu added

![image](https://user-images.githubusercontent.com/130473605/232338593-37c67b3d-3e87-46dc-9640-421278255dc7.png)


***NOTE***

Do not copy Verbatim - for obvious reasons, it can give sometimes you random information that isnt entirely correct
