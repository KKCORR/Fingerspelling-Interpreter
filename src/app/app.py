import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
import time

from app_video_capture import AppVideoCapture


class App:
    def __init__(self, window, window_title, delay=15, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = AppVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(
            window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Record Button
        self.is_record = False
        self.record_btn_text = tkinter.StringVar()
        self.record_btn = tkinter.Button(
            window, textvariable=self.record_btn_text, width=50, command=self.toggle_record)
        self.record_btn_text.set(self.get_record_btn_text(self.is_record))
        self.record_btn.pack(anchor=tkinter.CENTER, expand=True)

        # Output text from model
        self.output_text = tkinter.StringVar()
        self.output_text_label = tkinter.Label(
            window, textvariable=self.output_text, width=50)
        self.output_text.set("")
        self.output_text_label.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = delay
        self.update()

        self.window.mainloop()

    def get_record_btn_text(self, is_record):
        if is_record:
            return "Recording..."
        else:
            return "Click to record"

    def toggle_record(self):
        self.is_record = not self.is_record
        self.record_btn_text.set(self.get_record_btn_text(self.is_record))
        if not self.is_record:
            self.output_text.set("")

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(cv2.flip(frame, 1)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

            if self.is_record:
                current_text = self.output_text.get()
                if len(current_text) >= 10:
                    new_text = ""
                else:
                    new_text = current_text + ">"
                self.output_text.set(new_text)

        self.window.after(self.delay, self.update)


# Create a window and pass it to the Application object
App(tkinter.Tk(), "Real-time Thai fingerspelling interpreter")
