# Translation App

## Overview
The **Translation App** is a GUI-based tool built using **Tkinter** that allows users to perform:
- **Text to Text Translation**
- **Text to Speech Conversion**
- **Speech to Text Conversion**

It features an intuitive interface with dropdown menus for language selection, text input fields, and an animated GIF background for visual appeal. The app utilizes **Google Translate API (googletrans)** for text translations and **gTTS (Google Text-to-Speech)** for speech synthesis. Additionally, **SpeechRecognition** is used for audio-to-text conversion.

## Features
- **Multi-language support**: Select input and output languages from a predefined list.
- **Text Translation**: Translate text from one language to another using Google Translate.
- **Text-to-Speech**: Convert translated text into speech and play the audio.
- **Speech-to-Text**: Upload a WAV file and convert speech to text.
- **User-Friendly Interface**: Dropdown menus, buttons, and a help section make navigation easy.
- **Animated Background**: A GIF animation runs smoothly in the background.

## Installation
### Prerequisites
Ensure you have **Python 3.x** installed, along with the required dependencies:
```sh
pip install tkinter pillow googletrans==4.0.0-rc1 gtts pygame speechrecognition
```

### Running the App
1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Run the following command:
```sh
python main.py
```

## Usage
1. **Select a Conversion Type**: Choose between "Text to Text," "Text to Speech," or "Speech to Text".
2. **Provide Input**:
   - For "Text to Text," enter text and select source & target languages.
   - For "Text to Speech," enter text and select the language for speech.
   - For "Speech to Text," upload a WAV file for processing.
3. **Click Submit**: The app will process the input and display the result.
4. **Play Audio (if applicable)**: In "Text to Speech," the generated speech will be played automatically.

## Images of the app
Home page: 
![image](https://github.com/user-attachments/assets/d3dbf70c-e863-4dd0-af67-cd89c71f278c)

Window 2: 
![image](https://github.com/user-attachments/assets/0c047fd6-b13a-444c-9cc2-cb9b5201bf57)

Window 3: 
![image](https://github.com/user-attachments/assets/213693d4-84a6-49cf-8b14-4e1440c55b45)


## File Structure
```
translation_app/
│── main.py            # Main application script
│── lang.gif           # Animated background GIF
│── requirements.txt   # List of dependencies
```

## Dependencies
- **Tkinter** - GUI framework
- **Pillow** - Image handling for GIF animation
- **Googletrans** - Text translation
- **gTTS** - Text-to-speech conversion
- **Pygame** - Audio playback
- **SpeechRecognition** - Speech-to-text conversion

## Potential Security Concerns
1. **Google Translate API Calls**: Since the app uses the `googletrans` library, there might be issues if Google updates its API. Consider using an official Google Translate API key for production.
2. **Temporary Audio Files**: The app generates an `output_speech.mp3` file during text-to-speech conversion. The deletion mechanism is based on a delay, which may sometimes fail.
3. **Unvalidated User Input**: Input from text fields is processed without validation, which could lead to unexpected behavior.
4. **Missing Exception Handling for API Errors**: If the Google Translate API or SpeechRecognition fails due to network issues, the app may crash without proper handling.

## Future Improvements
- Add support for **real-time speech translation**.
- Implement **error handling** for API failures.
- Improve UI design with **better layout and styling**.
- Enhance **speech recognition accuracy** by integrating a better model.

## Acknowledgments
Special thanks to **Google Translate API**, **gTTS**, and **SpeechRecognition** for providing powerful translation and speech processing tools.

