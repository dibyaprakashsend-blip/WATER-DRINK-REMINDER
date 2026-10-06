import tkinter as tk
from PIL import Image, ImageTk
import json
import os
import sys


# =====================================================
# SETTINGS
# =====================================================

REMINDER_TIME = 10 * 60 * 1000   # 10 minutes


# =====================================================
# GET APPLICATION FOLDER
# =====================================================

def get_app_folder():

    # When running normally with Python
    if not getattr(sys, "frozen", False):

        return os.path.dirname(
            os.path.abspath(__file__)
        )

    # When running as an EXE
    return os.path.dirname(
        sys.executable
    )


APP_FOLDER = get_app_folder()


# =====================================================
# USER DATA FOLDER
# =====================================================

# Store settings inside the user's Windows profile

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
# IMAGE PATH
# =====================================================

IMAGE_FILE = os.path.join(
    APP_FOLDER,
    "thalapathy.jpg"
)


# =====================================================
# SAVE SETTINGS
# =====================================================

def save_settings(name):

    settings = {
        "name": name
    }

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            settings,
            file,
            indent=4
        )


# =====================================================
# LOAD SETTINGS
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

    # Remove normal Windows border
    root.overrideredirect(True)

    # Keep above other applications
    root.attributes(
        "-topmost",
        True
    )

    # Slight transparency
    root.attributes(
        "-alpha",
        0.97
    )

    root.configure(
        bg="#252526"
    )


    # =================================================
    # WINDOW POSITION
    # =================================================

    width = 340
    height = 430

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = screen_width - width - 25
    y = screen_height - height - 80

    root.geometry(
        f"{width}x{height}+{x}+{y}"
    )


    # =================================================
    # TITLE
    # =================================================

    title = tk.Label(
        root,
        text=f"Hey, {name}! 💧",
        font=("Arial", 20, "bold"),
        bg="#252526",
        fg="#FFD43B"
    )

    title.pack(
        pady=(15, 5)
    )


    # =================================================
    # MESSAGE
    # =================================================

    message = tk.Label(
        root,
        text="Did you drink water?",
        font=("Arial", 14, "bold"),
        bg="#252526",
        fg="white"
    )

    message.pack(
        pady=5
    )


    # =================================================
    # CHARACTER
    # =================================================

    try:

        image = Image.open(
            IMAGE_FILE
        )

        image.thumbnail(
            (180, 240)
        )

        character = ImageTk.PhotoImage(
            image
        )

        image_label = tk.Label(
            root,
            image=character,
            bg="#252526"
        )

        image_label.pack(
            pady=8
        )

    except Exception as error:

        image_label = tk.Label(
            root,
            text="💧",
            font=("Arial", 80),
            bg="#252526",
            fg="white"
        )

        image_label.pack(
            pady=30
        )

        print(
            "Image error:",
            error
        )


    # =================================================
    # SHOW REMINDER
    # =================================================

    def show_reminder():

        message.config(
            text="Did you drink water? 💧"
        )

        yes_button.config(
            state="normal"
        )

        later_button.config(
            state="normal"
        )

        root.deiconify()

        root.attributes(
            "-topmost",
            True
        )


    # =================================================
    # HIDE + SCHEDULE NEXT REMINDER
    # =================================================

    def hide_and_schedule():

        root.withdraw()

        root.after(
            REMINDER_TIME,
            show_reminder
        )


    # =================================================
    # YES BUTTON
    # =================================================

    def drank_water():

        message.config(
            text="Great job! 💧"
        )

        yes_button.config(
            state="disabled"
        )

        later_button.config(
            state="disabled"
        )

        root.after(
            2000,
            hide_and_schedule
        )


    # =================================================
    # LATER BUTTON
    # =================================================

    def remind_later():

        hide_and_schedule()


    # =================================================
    # BUTTON FRAME
    # =================================================

    button_frame = tk.Frame(
        root,
        bg="#252526"
    )

    button_frame.pack(
        pady=10
    )


    # =================================================
    # YES BUTTON
    # =================================================

    yes_button = tk.Button(
        button_frame,
        text="YES",
        command=drank_water,
        font=("Arial", 11, "bold"),
        bg="#FFD43B",
        fg="black",
        padx=18,
        pady=8,
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
        font=("Arial", 10),
        bg="#444444",
        fg="white",
        padx=10,
        pady=8,
        relief="flat",
        cursor="hand2"
    )

    later_button.pack(
        side="left",
        padx=5
    )


    # =================================================
    # ESC TO EXIT
    # =================================================

    root.bind(
        "<Escape>",
        lambda event: root.destroy()
    )


    # =================================================
    # FIRST REMINDER
    # =================================================

    # Show immediately for testing

    root.deiconify()


    # =================================================
    # START APP
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
    # ERROR
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
    # START
    # =================================================

    def start():

        name = name_entry.get().strip()

        if not name:

            error.config(
                text="Please enter your name."
            )

            return

        save_settings(
            name
        )

        setup.destroy()

        start_water_buddy(
            name
        )


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

    # First time user

    setup_screen()

else:

    # Returning user

    start_water_buddy(
        settings["name"]
    )