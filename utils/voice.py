import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Speak now...")

            # Adjust for background noise
            recognizer.adjust_for_ambient_noise(source, duration=1)

            # Listen to the microphone
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        # Convert speech to text
        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text

    except sr.WaitTimeoutError:
        return "No speech detected. Please try again."

    except sr.UnknownValueError:
        return "Sorry, I couldn't understand your voice."

    except sr.RequestError:
        return "Speech Recognition service unavailable."

    except Exception as e:
        print("Voice Error:", e)
        return f"Voice error: {str(e)}"