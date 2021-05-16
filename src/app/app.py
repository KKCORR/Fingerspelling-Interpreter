import tkinter
from tkinter import messagebox
import cv2
import PIL.Image
import PIL.ImageTk
import time
import xgboost as xgb

from app_video_capture import AppVideoCapture
from hand_thread import HandThread
from hand_landmark import HandLandmark


class App:
    def __init__(self, window, window_title, xgb_model, delay=15, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = AppVideoCapture(self.video_source)
        self.frame = None
        self.landmarks = None
        self.hand_landmarker = HandLandmark()

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(
            window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Show/Hide skeleton
        self.is_show_skeleton = tkinter.IntVar()
        self.skeleton_checkbox = tkinter.Checkbutton(window, text="Show hand skeleton",
                                                     variable=self.is_show_skeleton,
                                                     onvalue=1, offvalue=0)
        self.skeleton_checkbox.pack()

        # Show/Hide debug text
        self.is_debug = tkinter.IntVar()
        self.debug_checkbox = tkinter.Checkbutton(window, text="debug",
                                                  variable=self.is_debug,
                                                  onvalue=1, offvalue=0,
                                                  command=self.toggle_debug)
        self.debug_checkbox.pack()

        # Record Button
        self.is_record = False
        self.record_btn_text = tkinter.StringVar()
        self.record_btn = tkinter.Button(
            window, textvariable=self.record_btn_text, width=50, command=self.toggle_record)
        self.record_btn_text.set(self.get_record_btn_text(self.is_record))
        self.record_btn.pack(anchor=tkinter.CENTER, expand=True)

        # Output text from model
        self.debug_text = tkinter.StringVar()
        self.debug_text_label = tkinter.Label(
            window, textvariable=self.debug_text, width=50, font=("TH Sarabun New", 25))
        self.debug_text.set("")

        self.output_text = tkinter.StringVar()
        self.output_text_label = tkinter.Label(
            window, textvariable=self.output_text, width=50, font=("TH Sarabun New", 25))
        self.output_text.set("")
        self.output_text_label.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = delay
        self.update()

        # Define hand thread
        self.hand_thread = None

        # Load xgb model
        self.xgb_model = xgb_model

        # Letter queue
        self.letter_queue = []

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def toggle_debug(self):
        if self.is_debug.get():
            self.debug_text_label.pack(anchor=tkinter.CENTER, expand=True)
        else:
            self.debug_text_label.pack_forget()

    def get_record_btn_text(self, is_record):
        if is_record:
            return "Recording..."
        else:
            return "Click to record"

    def toggle_record(self):
        self.is_record = not self.is_record
        self.record_btn_text.set(self.get_record_btn_text(self.is_record))
        if self.is_record:
            # Start predictor thread
            self.hand_thread = HandThread(self)
            self.hand_thread.start()
            self.record_btn.configure(bg="#fc5656", fg="#ffffff")
        else:
            self.hand_thread.stop()
            self.output_text.set("")
            self.debug_text.set("")
            self.letter_queue = []

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.frame = cv2.flip(frame, 1)
            landmarked_frame = self.frame.copy()
            if self.is_show_skeleton.get():
                self.hand_landmarker.draw_landmarks(
                    landmarked_frame, self.landmarks)

            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(cv2.cvtColor(landmarked_frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

            if self.is_record:
                if self.is_debug:
                    self.debug_text.set(",".join(self.letter_queue[-15:]))

        self.window.after(self.delay, self.update)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.hand_thread:
                self.hand_thread.stop()
            self.window.destroy()


# Create a window and pass it to the Application object
xgb_model = xgb.Booster()
xgb_model.load_model('../models/xgb_model_linear.model')

App(tkinter.Tk(), "Real-time Thai fingerspelling interpreter", xgb_model)
