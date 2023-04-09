import tempfile
from pydub import AudioSegment
from pydub.playback import play
import openai
import os

# Set your API key
API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = API_KEY

def text_to_speech_espeak(text, lang='en-us', speed=175):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        temp_wav = f"{fp.name}.wav"
        cmd = f'espeak "{text}" -w {temp_wav} -v {lang} -s {speed}'
        os.system(cmd)

        # Load and play the synthesized speech
        speech = AudioSegment.from_wav(temp_wav)
        play(speech)
        print("Speech played.")

def transcribe_and_submit():
  # Open the MP3 file and send it to OpenAI's API
  audio_file = open("output.mp3", "rb")
  transcript = openai.Audio.transcribe("whisper-1", audio_file)

  # Print the transcript
  query = transcript.text
  print(query)
  model_engine = "gpt-3.5-turbo"

  # Generate a response
  completion = openai.ChatCompletion.create(
      model=model_engine,
      messages = [
        {"role": "system", "content": "You are a helpful assistant. Respond to every query to the best of your ability."},
        {"role": "user", "content": f"{query}"}
      ]
  )

  # Retrieve and print the summary
  text_to_speech_espeak(completion.choices[0].message.content)

