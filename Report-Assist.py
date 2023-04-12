import openai
import xml.etree.ElementTree as ET
import sys
import time


art="""
              ,---------------------------,
              |  /---------------------\  |
              | |                       | |
              | |     Report            | |
              | |      Writing          | |
              | |       Assistnat       | |
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
openai.api_key = "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"

# Initialize message history
message_history = [
    {"role": "user", "content": "You are a penetration test report writing technical assistant. "
                                 "Give me Penetration Test Report writeups for each vulnerability I give you. "
                                 "Provide a Description, Background, Risk, Impact and remediaton section. "
                                 "All respsonses must be highly technical in nature. show the commands "
                                 "used to check for this issue. Also include references of where you are getting this information."}]

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
        print("API is currently overloaded, your on a free plan so it can happen. Either try again or Upgrade (up to you )")
    except KeyboardInterrupt:
        print("\n\n**** You want to quit huh?....No problem ****")
        time.sleep(1)
        sys.exit()
    except Exception as e:
        print(f"Error: {e}")
        print("An error occured, im out...")

def get_plugin_name(nessus_file):
    """Parse the Nessus XML file and return a list of plugin names"""
    tree = ET.parse(nessus_file)
    root = tree.getroot()
    plugin_names = []
    for report in root.findall("./Report"):
        for host in report.findall("./ReportHost"):
            for item in host.findall("./ReportItem"):
                severity = item.find("risk_factor").text
                if severity in ["Critical", "High", "Medium", "Low"]:
                    description_for_check = item.get("pluginName")
                    plugin_names.append(description_for_check)
    return plugin_names

def search_for_vulns():
    """Search for vulnerabilities using GPT-3 API"""
    while True:
        print("\nSearch for Vulns Selected\nEnter a search term, be specific for best results")
        user_input = input("---Interactive--->: ")
        message_history.append({"role": "user", "content": f"{user_input}"})
        reply_answer = chat_with_gpt3(message_history)
        print(reply_answer, "\n\n")
        print("* - - - Next Vulnerability - - - *\n\n")
        #Remove the last input to clean the history
        del message_history[-1]

def import_nessus_file():
    """Import Nessus XML file and generate AI generated report writeups"""
    nessus_file = input("\n\nPlease enter filename: ")
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

def main():
        print("* - - - -  Technical Report Writing Assistant - - - - *\n")
        print("Do you want to search for Vulnerabilites or Import a Nessus File?\n\n")
        choice = input("""(1) - Search for Vulns \n(2) - Import Nessus File \n\n(1) or (2) : """)
        if choice == "1":
                search_for_vulns()
        if choice == "2":
                import_nessus_file()
        else:
                print("Invalid Choice, exiting....")

if __name__ == '__main__':
        main()

              
