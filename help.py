# Licensed under Server Side Public License. Please see LICENSE file for more information.
# Copyright 2023 (Spirit Wolf)


import openai
import speech_recognition as sr
import json
import time
import mac_say

TRIGGER_PHRASE = "help"
RESET_PHRASE = "reset"
STOP_PHRASE = "stop"


with open('openai.key', 'r') as f:
    openai.api_key = "".join(f.readlines()).strip()


class Gpt:
    def __init__(self):
        self.model_name = "gpt-4"
        self.system_prompt = "Respond to commands that have been transcribed from a voice command using a speech recognition model"
        self.reset()

    def ask(self, prompt):
        self.history.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(model=self.model_name, messages=self.history).choices[0].message.content
        self.history.append({"role": "assistant", "content": response})
        return response

    def reset(self):
        self.history = [{"role": "system", "content": self.system_prompt}]

gpt = Gpt()

r = sr.Recognizer()


def listen_for_audio(listen_seconds: int = 10) -> str:
    """Listens for audio from the microphone

    Returns:
        str: The recognized speech from the audio
    """
    try:
        with sr.Microphone() as audio_source:
            r.adjust_for_ambient_noise(audio_source, duration=0.05)
            say_out_loud("listening")
            audio2 = r.listen(audio_source, timeout=10, phrase_time_limit=listen_seconds)
            say_out_loud("parsing")
            object = r.recognize_vosk(audio2).lower()
            text = json.loads(object)
            return text['text']

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("unknown error occurred")
    except sr.WaitTimeoutError:
        print("No voice detected")


def send_statement(voice_request: str) -> str:
    """Sends a statement to ChatGPT for Processing

    Args:
        voice_request (str): The requests to send

    Returns:
        str: The response from ChatGPT
    """
    response = gpt.ask(voice_request)
    return response

def say_out_loud(response: str) -> None:
    """Convert the text to speech

    Args:
        response (str): Text to read out loud
    """
    mac_say.say(response)



def main():
    triggered = False

    while True:
        if not triggered:
            voice_request = listen_for_audio(listen_seconds=3)
            if voice_request == TRIGGER_PHRASE:
                triggered = True
            elif voice_request == RESET_PHRASE:
                say_out_loud("resetting context")
                gpt.reset()
            elif voice_request == STOP_PHRASE:
                say_out_loud("stopping")
                exit()
        else:
            triggered = False
            say_out_loud("yes?")
            voice_request = listen_for_audio()
            if voice_request == RESET_PHRASE:
                say_out_loud("resetting context")
                gpt.reset()
            elif voice_request == STOP_PHRASE:
                say_out_loud("stopping")
                exit()
            else:
                say_out_loud("thinking")
                if voice_request:
                    chat_gpt_response = send_statement(voice_request)
                    if chat_gpt_response:
                        say_out_loud(chat_gpt_response)


if __name__ == "__main__":
    main()
