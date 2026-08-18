import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Speak now...")

            # Reduce background-noise problems
            recognizer.adjust_for_ambient_noise(source, duration=1)

            # Listen for speech
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
        print("No speech detected.")
        return "No speech detected. Please try again."

    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return "Sorry, I couldn't understand your voice."

    except sr.RequestError as e:
        print("Speech recognition service error:", e)
        return "Speech Recognition service unavailable."

    except Exception as e:
        print("Voice Error:", e)
        return f"Voice error: {str(e)}"