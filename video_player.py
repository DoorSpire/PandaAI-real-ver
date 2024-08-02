import tkinter as tk
import pygame as pg
from tkinter import filedialog
from moviepy.editor import VideoFileClip

class VideoPlayer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Video Player")
        self.geometry("800x600")

        self.player = None

        self.create_widgets()

    def create_widgets(self):
        self.browse_button = tk.Button(self, text="Browse", command=self.browse_video)
        self.browse_button.pack()

    def browse_video(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.play(file_path)

    def play(self, file_path):
        if self.player:
            self.player.close()
            self.player = None

        self.player = VideoFileClip(file_path)

        icon_file = 'pandaaiicon.ico'
        icon = pg.image.load(icon_file)
        pg.display.set_icon(icon)
        
        pg.init()
        pg.display.set_caption("PandaAI Video Player: " + file_path)
        
        self.player.preview(fps=self.player.fps)