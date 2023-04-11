import openai
import xml.etree.ElementTree as ET

openai.api_key = ("---INSERT API KEY HERE---")

#Setting the scene here, it tells chatgpt what you are expecting and gets sent was the chat history with every request
message_history = [{"role": "user", "content": f"You are a penetration test report writing technical assistant. \
                                                Give me Penetration Test Report writeups for each vulnerability I give you. \
                                                Provide a Description, Background, Risk, Impact and remediaton section. \
                                                All respsonses must be highly technical in nature. show the commands \
                                                used to check for this issue"}]

def chat_with_gpt3(message_history):
        completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.5,
                messages=message_history
        )
        reply_content = completion.choices[0].message.content
        #print(reply_content)
        return reply_content

def get_plugin_name(nessus_file):
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

print("* - - - -  Technical Report Writing Assistant - - - - *\n")

print("Do you want to search for Vulnerabilites or Import a Nessus File?\n\n")
choice = input("""(1) - Search for Vulns \n
(2) - Import Nessus File \n\n(1) or (2) : """)

if choice == "1":
        while True:
                print("\nSearch for Vulns Selected\nEnter a search term, be specific for best results")
                user_input = input(">: ")
                message_history.append({"role": "user", "content": f"{user_input}"})
                reply_answer = chat_with_gpt3(message_history)
                print(reply_answer, "\n\n")
                print("* - - - Next Vulnerability - - - *\n\n")
                # Remove the last input to clean the history
                del message_history[-1]
elif choice == "2":
        nessus_file = input("\n\nPlease enter filename: ")
        plugin_Name = get_plugin_name(nessus_file)
        print("\n\nCompiling AI Generated Report Writeups for: \n")
        with open("issues.txt", "w") as f:
                for x in plugin_Name:
                        print("Issue:", x)
                        message_history.append({"role": "user", "content": f"{x}"})
                        plugin_list = chat_with_gpt3(message_history)
                        print("\n********ISSUE********", x, plugin_list, file=f, sep='\n')
                        del message_history[-1]

else:
        exit
              
