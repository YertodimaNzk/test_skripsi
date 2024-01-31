from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import tempfile
import os

# Get text input from the user
text_input = input("Enter the text you want to convert to speech: ")

# Create a gTTS object
tts = gTTS(text=text_input, lang='id')  # 'id' is the code for Indonesian language

# Convert the speech to an AudioSegment
speech_bytes = BytesIO()
tts.write_to_fp(speech_bytes)
speech_bytes.seek(0)
speech = AudioSegment.from_file(speech_bytes, format="mp3")

tempfile.tempdir = "D:/Skripsi/text to speech/speech"
os.makedirs(tempfile.tempdir, exist_ok=True)

# Play the generated speech
play(speech)
