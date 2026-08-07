import speech_recognition as sr

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak now...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:
        return "Sorry, I couldn't understand your voice."

    except sr.RequestError:
        return "Speech Recognition service unavailable."