import tkinter as tk
import vlc
import json
import os
import sys


# =====================================================
# SETTINGS
# =====================================================

# 10 minutes
REMINDER_TIME = 10 * 60 * 1000

# How long happy/sad video stays before hiding
RESULT_TIME = 5000


# =====================================================
# APPLICATION FOLDER
# =====================================================

def get_app_folder():

    if not getattr(sys, "frozen", False):
        return os.path.dirname(
            os.path.abspath(__file__)
        )

    return os.path.dirname(
        sys.executable
    )


APP_FOLDER = get_app_folder()


# =====================================================
# VIDEO FILES
# =====================================================

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)

    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        filename
    )


ENTER_VIDEO = resource_path("enter.mp4")
HAPPY_VIDEO = resource_path("happy.mp4")
SAD_VIDEO = resource_path("sad.mp4")


# =====================================================
# USER SETTINGS
# =====================================================

USER_FOLDER = os.path.join(
    os.environ["APPDATA"],
    "WaterBuddy"
)

os.makedirs(
    USER_FOLDER,
    exist_ok=True
)

SETTINGS_FILE = os.path.join(
    USER_FOLDER,
    "settings.json" 
)


# =====================================================
# SAVE USER NAME
# =====================================================

def save_settings(name):

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "name": name
            },
            file,
            indent=4
        )


# =====================================================
# LOAD USER NAME
# =====================================================

def load_settings():

    if not os.path.exists(
        SETTINGS_FILE
    ):
        return None

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return None


# =====================================================
# WATER BUDDY
# =====================================================

def start_water_buddy(name):

    root = tk.Tk()

    root.title(
        "Water Buddy"
    )

    # Remove normal Windows border
    root.overrideredirect(True)

    # Always stay above other windows
    root.attributes(
        "-topmost",
        True
    )

    # =================================================
    # SMALL WINDOW - BOTTOM RIGHT
    # =================================================

    width = 360
    height = 320

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = screen_width - width - 20
    y = screen_height - height - 70

    root.geometry(
        f"{width}x{height}+{x}+{y}"
    )

    root.configure(
        bg="#252526"
    )


    # =================================================
    # VIDEO AREA
    # =================================================

    video_frame = tk.Frame(
        root,
        bg="black",
        width=360,
        height=220
    )

    video_frame.pack(
        fill="both",
        expand=True
    )

    video_frame.pack_propagate(
        False
    )


    # =================================================
    # MESSAGE
    # =================================================

    message = tk.Label(
        root,
        text=f"Hey, {name}! Did you drink water? 💧",
        font=("Arial", 13, "bold"),
        bg="#252526",
        fg="white"
    )

    message.pack(
        fill="x",
        pady=(5, 3)
    )


    # =================================================
    # BUTTON FRAME
    # =================================================

    button_frame = tk.Frame(
        root,
        bg="#252526"
    )

    button_frame.pack(
        pady=(2, 8)
    )


    # =================================================
    # VLC PLAYER
    # =================================================

    player = vlc.MediaPlayer()


    # =================================================
    # PLAY VIDEO
    # =================================================

    def play_video(video_file):

        if not os.path.exists(
            video_file
        ):

            message.config(
                text="Video file not found!"
            )

            print(
                "Missing video:",
                video_file
            )

            return

        # Stop previous video
        player.stop()

        # Create VLC media
        media = vlc.Media(
            video_file
        )

        player.set_media(
            media
        )

        # Make sure Tkinter knows
        # the video window ID
        root.update()

        player.set_hwnd(
            video_frame.winfo_id()
        )

        # Start video
        player.play()


    # =================================================
    # HIDE + WAIT FOR NEXT REMINDER
    # =================================================

    def hide_and_schedule():

        # Stop current video
        player.stop()

        # Hide Water Buddy
        root.withdraw()

        # Enable buttons for next reminder
        yes_button.config(
            state="normal"
        )

        later_button.config(
            state="normal"
        )

        # Wait 10 minutes
        root.after(
            REMINDER_TIME,
            show_reminder
        )


    # =================================================
    # YES BUTTON
    # =================================================

    def drank_water():

        # Disable buttons
        yes_button.config(
            state="disabled"
        )

        later_button.config(
            state="disabled"
        )

        # Change message
        message.config(
            text="Good job! 💧😊"
        )

        # Play happy animation
        play_video(
            HAPPY_VIDEO
        )

        # After 5 seconds hide
        root.after(
            RESULT_TIME,
            hide_and_schedule
        )


    # =================================================
    # REMIND LATER BUTTON
    # =================================================

    def remind_later():

        # Disable buttons
        yes_button.config(
            state="disabled"
        )

        later_button.config(
            state="disabled"
        )

        # Change message
        message.config(
            text="Okay... 😔"
        )

        # Play sad animation
        play_video(
            SAD_VIDEO
        )

        # After 5 seconds hide
        root.after(
            RESULT_TIME,
            hide_and_schedule
        )


    # =================================================
    # YES BUTTON
    # =================================================

    yes_button = tk.Button(
        button_frame,
        text="YES 💧",
        command=drank_water,
        font=("Arial", 10, "bold"),
        bg="#FFD43B",
        fg="black",
        padx=15,
        pady=5,
        relief="flat",
        cursor="hand2"
    )

    yes_button.pack(
        side="left",
        padx=5
    )


    # =================================================
    # LATER BUTTON
    # =================================================

    later_button = tk.Button(
        button_frame,
        text="Remind me later",
        command=remind_later,
        font=("Arial", 9),
        bg="#444444",
        fg="white",
        padx=10,
        pady=5,
        relief="flat",
        cursor="hand2"
    )

    later_button.pack(
        side="left",
        padx=5
    )


    # =================================================
    # SHOW REMINDER
    # =================================================

    def show_reminder():

        # Reset message
        message.config(
            text=f"Hey, {name}! Did you drink water? 💧"
        )

        # Enable buttons
        yes_button.config(
            state="normal"
        )

        later_button.config(
            state="normal"
        )

        # Show window
        root.deiconify()

        # Bring to front
        root.attributes(
            "-topmost",
            True
        )

        root.lift()

        # Play entrance animation
        play_video(
            ENTER_VIDEO
        )


    # =================================================
    # ESCAPE = EXIT
    # =================================================

    root.bind(
        "<Escape>",
        lambda event: close_app()
    )


    # =================================================
    # CLOSE APPLICATION
    # =================================================

    def close_app():

        player.stop()

        root.destroy()


    root.protocol(
        "WM_DELETE_WINDOW",
        close_app
    )


    # =================================================
    # FIRST REMINDER
    # =================================================

    # Show immediately for testing
    show_reminder()


    # =================================================
    # START TKINTER
    # =================================================

    root.mainloop()


# =====================================================
# FIRST TIME SETUP
# =====================================================

def setup_screen():

    setup = tk.Tk()

    setup.title(
        "Water Buddy Setup"
    )

    setup.geometry(
        "400x320"
    )

    setup.resizable(
        False,
        False
    )


    # =================================================
    # TITLE
    # =================================================

    title = tk.Label(
        setup,
        text="💧 Water Buddy",
        font=("Arial", 24, "bold")
    )

    title.pack(
        pady=(30, 10)
    )


    # =================================================
    # DESCRIPTION
    # =================================================

    description = tk.Label(
        setup,
        text="Your personal water reminder",
        font=("Arial", 12)
    )

    description.pack(
        pady=5
    )


    # =================================================
    # NAME
    # =================================================

    label = tk.Label(
        setup,
        text="What is your name?",
        font=("Arial", 14)
    )

    label.pack(
        pady=(15, 5)
    )


    name_entry = tk.Entry(
        setup,
        font=("Arial", 14),
        width=25
    )

    name_entry.pack(
        pady=5
    )

    name_entry.focus()


    # =================================================
    # ERROR MESSAGE
    # =================================================

    error = tk.Label(
        setup,
        text="",
        fg="red"
    )

    error.pack(
        pady=5
    )


    # =================================================
    # START FUNCTION
    # =================================================

    def start():

        name = name_entry.get().strip()

        if not name:

            error.config(
                text="Please enter your name."
            )

            return

        # Save name
        save_settings(
            name
        )

        # Close setup
        setup.destroy()

        # Start Water Buddy
        start_water_buddy(
            name
        )


    # =================================================
    # START BUTTON
    # =================================================

    button = tk.Button(
        setup,
        text="START",
        command=start,
        font=("Arial", 12, "bold"),
        padx=30,
        pady=8,
        cursor="hand2"
    )

    button.pack(
        pady=10
    )


    setup.mainloop()


# =====================================================
# PROGRAM START
# =====================================================

settings = load_settings()


if settings is None:

    # First-time user
    setup_screen()

else:

    # Returning user
    start_water_buddy(
        settings["name"]
    )