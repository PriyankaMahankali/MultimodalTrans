import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, StringVar, OptionMenu
from PIL import Image, ImageTk, ImageSequence
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import pygame

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

instructions = ('Use this app to translate text or audio files.\n'
                'Steps:\n'
                '1. Select the desired conversion type.\n'
                '2. Follow the prompts for input and output.\n')

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Translation App")
        self.root.geometry("800x600")  # Set initial window size
        self.recording = False  # Flag to check if recording is in progress

        # Load the animated GIF
        self.gif_path = "lang.gif"
        self.frames = []
        self.frame_index = 0
        self.animation_running = False

        self.load_gif()

        # Create a canvas for the animated background
        self.canvas = tk.Canvas(root, width=self.root.winfo_width(), height=self.root.winfo_height())
        self.canvas.pack(fill="both", expand=True)

        # Display the first frame of the GIF as the background
        self.gif_label = self.canvas.create_image(0, 0, anchor="nw", image=self.frames[0])

        # Update canvas and GIF on window resize
        self.root.bind("<Configure>", self.on_resize)

        # Title block
        self.title_label = tk.Label(root, text="The Translator", font=("Georgia", 24, 'bold'), borderwidth=10, relief='raised', fg='white', bg='black')
        self.title_label.place(relx=0.5, rely=0.1, anchor="center")

        # Dropdown for conversion types
        self.selected_option = StringVar(root)
        self.selected_option.set("Select Conversion Type")  # Placeholder text

        self.option_menu = OptionMenu(root, self.selected_option, 
                                     "Text to Text", "Text to Speech", "Speech to Text")
        self.option_menu.config(font=("Arial", 20, 'bold'), bg='black', fg='white')
        self.option_menu.place(relx=0.5, rely=0.4, anchor="center")

        # Submit Button
        self.submit_button = tk.Button(root, text="Submit", font=("Arial", 20, 'bold'), borderwidth=5, relief='raised', fg='white', bg='black', command=self.handle_option)
        self.submit_button.place(relx=0.5, rely=0.5, anchor="center")

        # Help Button
        self.help_button = tk.Button(root, text="Help", font=("Arial", 18, 'bold'), borderwidth=5, relief='raised', fg='white', bg='black', command=self.show_help)
        self.help_button.place(relx=0.5, rely=0.6, anchor="center")

        # Start the animation automatically
        self.start_animation()

    def load_gif(self):
        try:
            self.gif = Image.open(self.gif_path)
            # Store the original PIL.Image frames for resizing later
            self.original_frames = [frame.copy() for frame in ImageSequence.Iterator(self.gif)]
            # Create ImageTk.PhotoImage objects for the first frame
            self.frames = [ImageTk.PhotoImage(self.original_frames[0])]
            self.animation_running = True
        except Exception as e:
            messagebox.showerror("Error", f"Could not load GIF: {str(e)}")
            self.animation_running = False

    def start_animation(self):
        if self.animation_running:
            self.animate_gif()

    def handle_option(self):
        option = self.selected_option.get()
        if option == "Text to Text":
            self.open_text_to_text_window()
        elif option == "Speech to Text":
            self.open_speech_to_text_window()
        elif option == "Text to Speech":
            self.open_text_to_speech_window()
        else:
            messagebox.showwarning("Warning", "Please select a valid option.")

    def open_text_to_text_window(self):
        top = Toplevel(self.root)
        top.title("Text to Text")

        # Source language selection
        tk.Label(top, text="Select source language:").pack(pady=10)
        self.source_lang = StringVar(top)
        self.source_lang.set("Select Source Language")
        source_lang_menu = OptionMenu(top, self.source_lang, *LANGUAGES.values())
        source_lang_menu.pack(pady=10)

        # Input text
        tk.Label(top, text="Enter text in source language:").pack(pady=10)
        self.source_text = tk.Text(top, height=10, width=50)
        self.source_text.pack(pady=10)

        # Target language selection
        tk.Label(top, text="Select target language:").pack(pady=10)
        self.target_lang = StringVar(top)
        self.target_lang.set("Select Target Language")
        target_lang_menu = OptionMenu(top, self.target_lang, *LANGUAGES.values())
        target_lang_menu.pack(pady=10)

        # Translate button
        tk.Button(top, text="Translate", command=self.translate_text).pack(pady=10)

    def open_text_to_speech_window(self):
        top = Toplevel(self.root)
        top.title("Text to Speech")

        # Text input
        tk.Label(top, text="Enter text to convert to speech:").pack(pady=10)
        self.text_to_speech = tk.Text(top, height=10, width=50)
        self.text_to_speech.pack(pady=10)

        # Language selection
        tk.Label(top, text="Select Language:").pack(pady=10)
        self.speech_lang = StringVar(top)
        self.speech_lang.set("Select Language")
        speech_menu = OptionMenu(top, self.speech_lang, *LANGUAGES.values())
        speech_menu.pack(pady=10)

        # Generate button
        tk.Button(top, text="Generate Speech", command=self.text_to_speech_conversion).pack(pady=10)

    def open_speech_to_text_window(self):
        top = Toplevel(self.root)
        top.title("Speech to Text")

        tk.Label(top, text="Upload a WAV file for speech to text conversion:").pack(pady=10)
        tk.Button(top, text="Upload WAV File", command=self.upload_audio_for_speech_to_text).pack(pady=10)

    def translate_text(self):
        source_text = self.source_text.get("1.0", tk.END).strip()
        source_language = self.source_lang.get()
        target_language = self.target_lang.get()

        if not source_text:
            messagebox.showwarning("Warning", "Please enter some text.")
            return

        if source_language in LANGUAGES.values() and target_language in LANGUAGES.values():
            source_lang_code = [key for key, value in LANGUAGES.items() if value == source_language][0]
            target_lang_code = [key for key, value in LANGUAGES.items() if value == target_language][0]
            try:
                translator = Translator()
                translated = translator.translate(source_text, src=source_lang_code, dest=target_lang_code)
                messagebox.showinfo("Translated Text", f"Translated: {translated.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Translation failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select valid languages.")

    def text_to_speech_conversion(self):
        text = self.text_to_speech.get("1.0", tk.END).strip()
        language = self.speech_lang.get()

        if not text:
            messagebox.showwarning("Warning", "Please enter some text.")
            return

        if language in LANGUAGES.values():
            lang_code = [key for key, value in LANGUAGES.items() if value == language][0]
            
            try:
                # Translate the text to the selected language
                translator = Translator()
                translated = translator.translate(text, dest=lang_code)
                translated_text = translated.text

                # Generate speech from the translated text
                tts = gTTS(text=translated_text, lang=lang_code)
                output_path = "output_speech.mp3"
                tts.save(output_path)

                # Play the generated speech
                pygame.mixer.music.load(output_path)
                pygame.mixer.music.play()

                # Schedule file deletion after playback
                self.root.after(int(pygame.mixer.music.get_pos() + 2000), os.remove, output_path)

                messagebox.showinfo("Success", "Speech is playing.")
            except Exception as e:
                messagebox.showerror("Error", f"Text-to-speech conversion failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select a valid language.")

    def upload_audio_for_speech_to_text(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
        if file_path:
            try:
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                with sr.AudioFile(file_path) as source:
                    audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio)
                    messagebox.showinfo("Converted Text", text)
            except Exception as e:
                messagebox.showerror("Error", f"Speech-to-text conversion failed: {str(e)}")

    def show_help(self):
        messagebox.showinfo("Help", instructions)

    def animate_gif(self):
        # Resize the GIF frame to fill the screen
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Resize the frame with high-quality downsampling
        resized_frame = self.original_frames[self.frame_index].resize((canvas_width, canvas_height), Image.LANCZOS)
        frame_image = ImageTk.PhotoImage(resized_frame)

        # Update the canvas with the next frame of the GIF
        self.canvas.itemconfig(self.gif_label, image=frame_image)
        self.root.after(100, self.animate_gif)  # Adjust the speed of animation

        # Store the resized frame to avoid garbage collection
        self.canvas.image = frame_image

        self.frame_index = (self.frame_index + 1) % len(self.original_frames)


    def on_resize(self, event):
        # Update the canvas size and redraw the GIF
        self.canvas.config(width=event.width, height=event.height)
        if not self.animation_running:
            self.start_animation()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
