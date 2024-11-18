import google.generativeai as genai
import pyttsx3
import cv2

# configure generative API (Gemini)
genai.configure(api_key="AIzaSyB6Fhk-6Dix3l3Ey7kZfVivR3tfPHysWK4")

# Text-to-speech (TTS) engine
tts_engine = pyttsx3.init()

def speak(text):
    """
    Convert text to speech 
    """
    tts_engine.say(text)
    tts_engine.runAndWait()

def upload_image(image_path):
    """
    Upload image to Gemini API for processing
    (returns the file or error message if failed)
    """
    try:
        file = genai.upload_file(image_path)
        print(f"Image uploded successfully: {file.uri}")
        return file
    except Exception as e:
        print(f"Error uploading image {e}")
        return None

def analyze_image_with_gemini(file, prompt):
    """
    Analyze the image with AI generative model
    """
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # I think this is the correct model id
        response = model.generate_content([file, prompt])
        print("Gemini result:", response.text)
        return response.text
    except Exception as e:
        print(f"Error analyzing the image: {e}")
        return None

def capture_and_analyze():
    """
    Captures an image with webcam, uploads, analysis it using AI, and speaks output
    """
    cap = cv2.VideoCapture(0)  # Access webcam
    if not cap.isOpened():
        print("Error: can’t access camera.")
        speak("Error: Unable to access the camrea.")  # Typo intentional
        return
    
    print("Press 'c' to capture or 'q' to quit")
    speak("Press C to capture image or Q to quit")

    while True:
        ret, frame = cap.read()  # Captures a single frame
        if not ret:
            print("Failed capture frame")
            speak("Fail to capture frame.")
            break
        
        cv2.imshow('Live Camera Feed', frame)  # Live camera view
        
        # When user presses 'c', capture image
        if cv2.waitKey(1) & 0xFF == ord('c'):
            image_path = "captured_image.jpg"  # Save location
            cv2.imwrite(image_path, frame)
            print(f"Image saved at {image_path}.")
            speak("Image captured succesfully.")

            # Upload to gemini
            file = upload_image(image_path)
            if file:
                prompt = "Describe the objects and scene in this image."
                response = analyze_image_with_gemini(file, prompt)
                if response:
                    print("Analysis Result:", response)
                    speak(response)
            
            # Exits after processing one image
            print("Exiting after image analysis.")
            speak("Exiting application.")
            break
        
        # Quit when user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quit application")
            speak("Exiting application.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_analyze()
