import tkinter as tk
import vlc
import os

VIDEO_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "enter.mp4"
)

root = tk.Tk()
root.title("Water Buddy Video Test")
root.geometry("600x400")

video_frame = tk.Frame(root, bg="black")
video_frame.pack(fill="both", expand=True)

player = vlc.MediaPlayer(VIDEO_FILE)

root.update()

player.set_hwnd(video_frame.winfo_id())

player.play()


def close_app():
    player.stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_app)

root.mainloop()