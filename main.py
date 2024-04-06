import requests
import customtkinter as ctk
import tkinter as tk
import pyautogui as pwt
import pywhatkit as pwtk
import threading
import datetime
import time
import APIKeys
from AppOpener import open

API_URL_CHATBOT = "https://api-inference.huggingface.co/models/MRF18/chatbot"
API_URL_EMOTION = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-emotion"
API_KEY = f"{APIKeys.API_Key_1}"  #Include your own API Key here

class SongGenie:
    def __init__(self):
        self.setup_main_window()

    def setup_main_window(self):
        # Setup main window
        self.Main_Window = ctk.CTk()
        self.Main_Window.title('SongGenie')
        self.Main_Window.geometry('700x550')
        self.Main_Window.minsize(700, 550)
        self.Main_Window.maxsize(700, 550)
        self.create_menu()

    def create_menu(self):
        # Create menu
        Menu = ctk.CTkFrame(self.Main_Window, width=200, height=600)
        Menu.place(x=0, y=0)
        ctk.CTkLabel(Menu, text='SongGenie', padx=0, pady=0, font=("San Francisco", 35)).place(x=17, y=10)
        ctk.CTkLabel(Menu, text='Menu', padx=0, pady=0, font=("San Francisco", 25)).place(x=17, y=100)
        ctk.CTkButton(Menu, text="New Chat", command=self.start).place(x=17, y=150)
        ctk.CTkLabel(Menu, text='Play On', padx=0, pady=0, font=("San Francisco", 25)).place(x=17, y=200)
        self.platform = "Youtube"
        optionmenu = ctk.CTkOptionMenu(Menu, values=["Spotify", "Youtube"], command=self.play_on)
        optionmenu.place(x=17, y=250)
        optionmenu.set("Youtube")
        ctk.CTkLabel(Menu, text='Song', padx=0, pady=0, font=("San Francisco", 25)).place(x=17, y=300)
        self.globaltext = ""
        ctk.CTkButton(Menu, text="Play", command=self.song_playing).place(x=17, y=350)
        ctk.CTkLabel(Menu, text='Theme', padx=0, pady=0, font=("San Francisco", 25)).place(x=17, y=400)
        optionmenu = ctk.CTkOptionMenu(Menu, values=["System", "Dark", "Light"], command=self.set_theme)
        optionmenu.place(x=17, y=450)
        optionmenu.set("System")

    def set_theme(self, choice):
        # Set theme
        ctk.set_appearance_mode(choice)

    def play_on(self, choice):
        # Set platform for playing songs
        self.platform = choice

    def start(self):
        # Start chat
        self.txt = ctk.CTkTextbox(self.Main_Window, width=800, height=580)
        self.txt.place(x=200, y=0)
        self.txt.insert(tk.END, "\n" + self.get_greeting())
        self.entry = ctk.CTkEntry(self.Main_Window, placeholder_text="Message SongGenie", width=400)
        self.entry.place(x=210, y=500)
        self.main_button_1 = ctk.CTkButton(self.Main_Window, text="Send", fg_color="transparent", border_width=2,text_color=("gray10", "#DCE4EE"), width=75, command=self.Text).place(x=620,y=500)

    def get_greeting(self):
        # Get greeting message based on time of day
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            return "Good Morning!!, How is your day going?"
        elif 12 <= hour < 16:
            return "Good Afternoon!!, How is the day going?"
        else:
            return "Good Evening!!, How has your day been?"

    def Text(self):
        # Process user input
        self.txt.configure(state="normal")
        text = self.entry.get()
        self.globaltext += text
        self.txt.insert(tk.END, "\n" + text)
        self.txt.configure(state="disabled")
        self.entry.delete(0, 'end')
        threading.Thread(target=self.chatting(text), args=(text,)).start()

    def chatting(self,text):
        try:
            if text.strip():  # Check if the input is not empty
                headers = {"Authorization": f"Bearer {API_KEY}"}
                payload = {"inputs": text}
                response = requests.post(API_URL_CHATBOT, headers=headers, json=payload).json()
                chat = response[0]["generated_text"]
                self.txt.configure(state="normal")
                self.txt.insert(tk.END, "\n" + chat)
                self.txt.configure(state="disabled")
                self.entry.delete(0, 'end')
        except Exception as e:
            self.txt.configure(state="normal")
            self.txt.insert(tk.END, "\n" + f"An error occurred: {e}")
            self.txt.configure(state="disabled")
            self.entry.delete(0, 'end')

    def get_song_for_emotion(self, emotion):
        if emotion == "sadness":
            return "positive mood booster songs"
        elif emotion == "joy":
            return "joyful songs"
        elif emotion == "love":
            return "love songs"
        elif emotion == "anger":
            return "nostalgic songs playlist"
        elif emotion == "fear":
            return "soft pop songs"
        elif emotion == "surprise":
            return "rap songs"

    def platform_player(self, song):
        # Play song based on platform
        if self.platform == "Youtube":
            self.play_on_youtube(song)
        elif self.platform == "Spotify":
            self.play_spotify(song)

    def play_spotify(self, text):
        # Play song on Spotify
        try:
            open("spotify", match_closest=True)
            time.sleep(5)
            pwt.hotkey("ctrl", "l")
            time.sleep(2)
            pwt.write(f"{text}", interval=0.1)
            Keys = ["enter", "tab", "enter", "enter"]
            for key in Keys:
                time.sleep(2)
                pwt.press(key)
            time.sleep(2)
            pwt.hotkey("ctrl", "r")
        except Exception as e:
            self.txt.configure(state="normal")
            self.txt.insert(tk.END, "\n" + f"An error occurred: {e}")
            self.txt.configure(state="disabled")
            self.entry.delete(0, 'end')

    def play_on_youtube(self, text):
        # Play song on YouTube
        pwtk.playonyt(text)

    def song_playing(self):
        try:
            text = self.globaltext.strip()
            if text == "":
                song_type = "Never Gonna Give You up"
                self.platform_player(song_type)
            else:
                headers = {"Authorization": f"Bearer {API_KEY}"}
                payload = {"inputs": f"{text}"}
                response = requests.post(API_URL_EMOTION, headers=headers, json=payload).json()
                emotion = response[0]["generated_text"]
                song_type = self.get_song_for_emotion(emotion)
                self.platform_player(song_type)
        except Exception as e:
            self.txt.configure(state="normal")
            self.txt.insert(tk.END, "\n" + f"An error occurred: {e}")
            self.txt.configure(state="disabled")
            self.entry.delete(0, 'end')

# Main program
if __name__ == "__main__":
    Genie = SongGenie()
    Genie.Main_Window.mainloop()