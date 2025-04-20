import speech_recognition as sr

import sys
sys.path.insert(0, r"dev_env\Lib\site-packages")
import ollama

#Creating a recognizer object and listing the available sound devices. 
recognizer = sr.Recognizer()
devices = sr.Microphone.list_microphone_names()
print(f"Listing sound devices: {devices[:5]}")

#Choosing the 3rd input device
device_index = 2

try:
    context = "You are Rick, the interview preparation assistant. Respond to the user requests via brief responses, unless explicitly stated otherwise. If asked for a code example, provide a sample output with the program as well."
    message = [{'role':'system','content':context}]

    with sr.Microphone(device_index=device_index) as source:
        print(f"Using Microphone: {devices[device_index]}")

        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Adjusted for background noise")

        while True:
            print("\nListening.....")

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit = 10)
                print("Processing.....")
                text = recognizer.recognize_google(audio)
                print("Recognizer: ", text)

                #Exit program if user says "bye"
                if 'bye' in text.lower():
                    break
                
                #Append user's input and provide output
                messages = message.append({'role':'user', 'content':text})
                response = ollama.chat(
                    model = "deepseek-coder",
                    messages = messages
                )

                print(response['message']['content'])

            except sr.WaitTimeoutError:
                print("No speech detected. Retrying....")
        
            except sr.UnknownValueError:
                print("Could not interpret the audio. Trying again....")

except IndexError:
    print("Invalid input device!")

except Exception as e:
    print(f"Error: {e}")
