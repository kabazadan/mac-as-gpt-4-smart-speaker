# mac-as-gpt-4-smart-speaker

This project converts your Mac to a smart speaker. Use the phrase "help", and it will respond with "Yes?". Then, you can ask it anything and it will speak a response from GPT-4.

### Setup

This requires that you have a mac.

Install requirements.

```
pip3 install -r requirements.pip
```

Download a speech recognition model and unzip it as a folder named `model` in this project's directory.
The speech recognition model can be found here: https://alphacephei.com/vosk/models

You will need to create an API key that has GPT-4 enabled, and paste it in a file named "openai.key".

You will also need to install pyaudio. I found the following Stack Overflow response helpful for this: https://stackoverflow.com/a/33851618



### Starting the app

Start the app as follows:

```
python3 help.py
```

### Speech commands

The bot will say 'listening' when it is listening for you to say something. It will say 'parsing' to indicate it is trying to convert your speech to text.

#### 'help'

Once it is listening, the 'help' phrase triggers the app to start listening for a command. It lets you know that it's ready for a command by saying 'Yes?'.

Then, it will say 'thinking' to let you know that it is asking GPT-4 for a response. Once it has received a response, it will speak it to you.

#### 'reset'

By default, the app will keep a track of your conversation history. You can say 'reset' to delete the conversation you've had with it so far, to start a new one.

#### 'stop'

This will tell the app to exit.
