"""This module is responsible for playing text to speech messages."""

import pyttsx3


def tts(text: str) -> None:
    """
    This function takes in a message and plays it using pyttsx3.
    It requires a parameter string which is to be played when 
    function is called.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
