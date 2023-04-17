import openai
import xml.etree.ElementTree as ET
import sys
import time
import signal
import re
import itertools

art="""
              ,---------------------------,
              |  /---------------------\  |
              | |                       | |
              | |     Report            | |
              | |      Writing          | |
              | |       Assistant       | |
              | |                       | |
              |  \_____________________/  |
              |___________________________|
            ,---\_____     []     _______/------,
          /         /______________\           /|
        /___________________________________ /  | ___
        |                                   |   |    )
        |  _ _ _                 [-------]  |   |   (
        |  o o o                 [-------]  |  /    _)_
        |__________________________________ |/     /  /
    /-------------------------------------/|      ( )/
  /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"""

print(art)
time.sleep(1)

# Set OpenAI API key
openai.api_key = ""  # INSERT API KEY HERE, NOT BELOW!

# Check API Key
def check_api_key():
        if openai.api_key == "":
            correct_APIKey = input("API Key Not Set - will be in the format sk-*********. Please enter it now: ")
            openai.api_key = correct_APIKey
        else:
            api_check = r"^sk-[a-zA-Z0-9]*$"
            if re.match(api_check, openai.api_key):
                print("\nLooks like you have added an API Key of the correct format...continuing")
            else:
                update_apiKey = input("API Key doesn't match the correct format, please re-enter it now \nin the format sk-***********: ")
                print(f"API Key entered is: {update_apiKey}")
                input("Press Enter to continue....")
                openai.api_key = update_apiKey

print("* - - - -  Technical Report Writing Assistant - - - - *\n")
check_api_key()

# Initialize message history
message_history = [
    {"role": "user", "content": "You are a penetration test report writing technical assistant. "
                                 "Give me Penetration Test Report writeups for each vulnerability I give you. "
                                 "Provide a Description, Background, Risk, Impact and Remediaton section. "
                                 "All respsonses must be highly technical in nature. show the commands "
                                 "used to check for this issue."}]

def chat_with_gpt3(message_history):
    """Chat with GPT-3 API and return the response content"""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=message_history
        )
        reply_content = completion.choices[0].message.content
        return reply_content

    except openai.error.RateLimitError as e:
        print(f"Error: {e}")
        print("API is currently overloaded, you're on a free plan so it can happen. Either try again or Upgrade (up to you )")
        main()
    except KeyboardInterrupt:
        print("\n\n**** You want to quit huh?....No problem ****\n\n")
        time.sleep(1)
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("An error occured, im out...")
        main()

def get_plugin_name(nessus_file):
    """Parse the Nessus XML file and return a list of plugin names"""
    tree = ET.parse(nessus_file)
    root = tree.getroot()
    # Initialise an empty list
    plugin_names = []
    for report in root.findall("./Report"):
        for host in report.findall("./ReportHost"):
            for item in host.findall("./ReportItem"):
                severity = item.find("risk_factor").text
                if severity in ["Critical", "High", "Medium", "Low"]:
                    description_for_check = item.get("pluginName")
                    # check for duplicates
                    if description_for_check not in plugin_names:
                        plugin_names.append(description_for_check)
    return plugin_names

def search_for_vulns():
    """Search for vulnerabilities using GPT-3 API"""
    while True:
        user_input = input("---Interactive--->: ")
        if user_input == "exit":
            print("Quit requested....exiting\n")
            time.sleep(0.5)
            main()
        else:
            message_history.append({"role": "user", "content": f"{user_input}"})
            print("Gathering Information from API....\n\n")
            reply_answer = chat_with_gpt3(message_history)
            print(reply_answer, "\n\n")
            print("\n* - - - Next Vulnerability - - - *\n\n[type \"exit\" to return to main menu]\n")
            # Remove the last input to clean the history
            del message_history[-1]

def import_nessus_file():
    """Import Nessus XML file and generate AI generated report writeups"""
    nessus_file = input("\n\nPlease enter filename: (Must be in Current Working Directory) ")
    saved_file = input("\n\nPlease enter filename to save genearated output as: (i.e Inf-report.txt) ")
    plugin_names = get_plugin_name(nessus_file)
    print("\n\nCompiling AI Generated Report Writeups for: \n")
    with open(saved_file, "w") as f:
                for x in plugin_names:
                        print("Issue:", x)
                        message_history.append({"role": "user", "content": f"{x}"})
                        plugin_list = chat_with_gpt3(message_history)
                        print("\n********ISSUE********", x, plugin_list, file=f, sep='\n')
                        del message_history[-1]

def signal_handler(signal, frame):
    print('\n\nYou pressed Ctrl+C!')
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

def main():
        print("\nDo you want to search for Vulnerabilites or Import a Nessus File?\n\n")
        choice = input("""(1) - Search for Vulns \n(2) - Import Nessus File \n\n(1) or (2) : """)
        if choice == "1":
                print("\nSearch for Vulns Selected\nEnter a search term, be specific for best results - Type \"exit\" to return to menu\n")
                search_for_vulns()
        elif choice == "2":
                import_nessus_file()
        else:
                print("Invalid Choice, exiting....")

if __name__ == '__main__':
        main()



              
