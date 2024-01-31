import pyttsx3

import pyttsx3

# Install eSpeak voices for Indonesian (if not already installed)
# https://github.com/espeak-ng/espeak-ng/wiki/Installing-voices

# Initialize the text-to-speech engine
engine = pyttsx3.init('espeak-ng')

# Set the language to Indonesian
# print(engine.getProperty('voices'))
# engine.setProperty('voice', 'id')  # Assuming you have an Indonesian voice installed

# text = input("Enter the text to speak: ")

# # Speak the text
# engine.say(text)
# engine.runAndWait()


# # Get text input from the user
# #text_input = input("Enter the text you want to convert to speech: ")

# # Initialize the text-to-speech engine
# # engine = pyttsx3.init()

# # for voice in engine.getProperty('voices'):
# #     print(voice)
    
# # Set properties (optional)
# # engine.setProperty('rate', 120)  # Speed of speech
# # #engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

# # # Convert text to speech and play it
# # engine.say(text_input)
# # engine.runAndWait()


# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# # Get all available voices
voices = engine.getProperty('voices')

# Print information about each voice
for voice in voices:
    print("ID:", voice.id)
    print("Name:", voice.name)
    print("Languages:", voice.languages)
    print("Gender:", voice.gender)
    print("Age:", voice.age)
    print("")

# # Optionally, you can print the supported languages without other details
# supported_languages = set()
# for voice in voices:
#     try:
#         supported_languages.update(voice.languages)
#     except IndexError:
#         pass

# print("Supported Languages:", supported_languages)
