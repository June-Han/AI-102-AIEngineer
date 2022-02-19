'''
Notes:
Python-dotenv is a Python module that allows you to specify 
environment variables in traditional UNIX-like “.env” (dot-env) 
file within your Python project directory

The dotenv is a zero-dependency module that loads environment 
variables from a . env file into process. env . Storing 
configuration in the environment separate from code is 
based on the Twelve-Factor App methodology.
'''
from email.mime import audio
from fileinput import filename
from dotenv import load_dotenv
from datetime import datetime
import os
from playsound import playsound

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config

        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
        print('Ready to use speech service in:', speech_config.region)

        # Get spoken input
        command = TranscribeCommand()
        if command.lower() == 'what time is it?':
            TellTime()

    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''
    
    '''
    # Configure speech recognition using microphone
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now...')
    '''

    # Configure Speech Recognition using audiofile
    audioFile = 'time.wav'
    playsound(audioFile)
    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    
    # Process speech input
    #Get the speech from voice
    speech = speech_recognizer.recognize_once_async().get()
    '''
    # If the speech variable is Reason.RecognisedSpeech
    # So the result is:
    # Reason.RecognisedSpeech == Reason.RecognisedSpeech
    '''
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
        print(cancellation.error_details)


    # Return the command
    return command

'''
# Function for speech synthesis
'''
def TellTime():
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)

    # Configure speech synthesis 
    # Able to change voice to male RyanNeural vs Female LibbyNeural
    speech_config.speech_synthesis_voice_name = "en-GB-LibbyNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

    # Synthesize spoken output
    # Read aloud the response text through the computer speakers
    speak = speech_synthesizer.speak_text_async(response_text).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()