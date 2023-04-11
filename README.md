# AI-Report-Assistant
Harness the Power of AI for all your reporting needs.

Mainly came about as I wanted to generate a decent Knowledge Base and trying to save time when Googling for issues.

Its just a Python tool for interacting with the chatgpt api. 
* Uses the gpt-3.5-turbo model. 
* Temperature is set to 0.5 (see https://www.atmosera.com/ai/understanding-chatgpt/)
* Only dependency is `openai`

`pip install openai`

Sign into chatgpt and get an API Key - You get $5 free. It costs about $0.002 per API request so free credit will probably expire before you use up that amount.

# How to use

You can use it interactively to get writeups for a single issue or pass it a .nessus file and it will parse it, pulling all Critical, High, Medium and Low Issues then using the pluginName as input to get writeups. 

All issues are then saved in an issues.txt file.


Run with `python3 Report-Assist.py`

## Nessus File
If passing a nessus file choose option 2 and give it the filename.

![image](https://user-images.githubusercontent.com/130473605/231190133-792e141b-490e-4660-afcc-f790f4c4db15.png)


issues.txt file should then be in current directory.

![image](https://user-images.githubusercontent.com/130473605/231189144-aca8f1f6-f6af-478a-b418-7c6f1231b717.png)


## Interactive Mode

Try to be specific for best results. If choosing option 1 just give it the issue ie `>: SMB Signing enabled but not required on Windows 10 host` 

![image](https://user-images.githubusercontent.com/130473605/231189885-3081e673-2ef5-40a6-ad71-68c7213fc83e.png)


***NOTE***

Do not copy Verbatim - for obvious reasons, it can give sometimes you random information that isnt entirely correct
