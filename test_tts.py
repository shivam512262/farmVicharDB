import requests

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"
OUTPUT_FILENAME = "marathi_speech.mp3" # Changed filename for clarity

def test_tts_endpoint(text, language):
    """Calls the TTS endpoint with a POST request and saves the audio."""
    print(f"--- Testing TTS for language: {language} ---")
    url = f"{BASE_URL}/api/tts/synthesize"
    
    payload = {
        "text": text,
        "language": language
    }
    
    print(f"Sending text: '{text}'")
    
    try:
        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()
            
            with open(OUTPUT_FILENAME, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Success! Audio saved to '{OUTPUT_FILENAME}'")
            
    except requests.exceptions.RequestException as err:
        error_details = err.response.text if err.response else str(err)
        print(f"❌ TTS Test Failed! Error: {error_details}")

# --- Main Execution ---
if __name__ == "__main__":
    
    # Updated with the Marathi text from your example
    text_to_synthesize = "मराठी भाषा ही इंडो-युरोपीय भाषाकुळातील एक भाषा आहे. मराठी ही भारताच्या २२ अधिकृत भाषांपैकी एक आहे. मराठी महाराष्ट्र राज्याची अधिकृत, तर गोवा राज्याची सह-अधिकृत भाषा आहे. २०११ च्या जनगणनेनुसार, भारतात मराठी भाषकांची एकूण लोकसंख्या सुमारे १४ कोटी आहे. मराठी मातृभाषा असणाऱ्या लोकांच्या संख्येनुसार मराठी ही जगातील १०वी व भारतातील ३री भाषा आहे. मराठी भाषा भारताच्या प्राचीन भाषांपैकी एक असून, महाराष्ट्री प्राकृतचे आधुनिक रूप आहे. मराठीचे वय सुमारे २४०० वर्षे आहे"
    language_to_use = "marathi"
    
    test_tts_endpoint(text_to_synthesize, language_to_use)

