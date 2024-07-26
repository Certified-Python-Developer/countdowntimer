from tkinter import *
import tkinter as tk

class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.createWidgets()
        
        self.master.geometry("500x200")
        self._alarm_id = None
        self._paused = False
        self._starttime = 0
        self.time_in_seconds = 0
    
    def createWidgets(self):
        self.someFrame = Frame(self)
        self.time_var = StringVar()
        self.input_time = tk.Entry(self, width=25, font=('Calibri',12), textvariable=self.time_var)
        self.input_time.insert(0, "Enter Time (e.g., 1s, 1m, 1h)")
        self.input_time.pack(padx=10, pady=(30,10))
        self.input_time.bind("<Button-1>", self.enter)
        
        self.startButton = Button(self.someFrame, text="Start", font=('Helvetica',12), bg='green', fg='white', command=self.startTime)
        self.startButton.pack(side=LEFT, padx=5)

        self.pauseButton = Button(self.someFrame, text="Pause", font=('Helvetica',12), bg='azure', command=self.pauseTime)
        self.pauseButton.pack(side=LEFT, padx=5)

        self.resetButton = Button(self.someFrame, text="Reset", font=('Helvetica',12), bg='azure', command=self.resetTime)
        self.resetButton.pack(side=LEFT, padx=5)

        self.closeButton = Button(self.someFrame, text="Close", font=('Helvetica',12), bg='red',fg='white', command=self.closeApp)
        self.closeButton.pack(side=LEFT, padx=5)
        self.someFrame.pack(side=TOP)

        self.labelvariable = StringVar()
        self.labelvariable.set("")

        self.thelabel = Label(self, textvariable=self.labelvariable, font=('Helvetica',50))
        self.thelabel.pack(side=TOP)

    def enter(self, *args):
        self.input_time.delete(0, 'end')
        
    def startTime(self):
        self.get_time = self.time_var.get().strip()
        if self.get_time.endswith('s'):
            self.time_in_seconds = int(self.get_time[:-1])
        elif self.get_time.endswith('m'):
            self.time_in_seconds = int(self.get_time[:-1]) * 60
        elif self.get_time.endswith('h'):
            self.time_in_seconds = int(self.get_time[:-1]) * 3600
        else:
            try:
                self.time_in_seconds = int(self.get_time)
            except ValueError:
                self.time_in_seconds = 0
        
        self._starttime = self.time_in_seconds
        self._paused = False
        if self._alarm_id is None:
            self.countdown(self._starttime)

    def pauseTime(self):
        if self._alarm_id is not None:
            self._paused = True

    def resetTime(self):
        if self._alarm_id is not None:
            self.master.after_cancel(self._alarm_id)
            self._alarm_id = None
            self._paused = False
            self.countdown(0)
            self._paused = True
    
    def closeApp(self):
        self.master.destroy()

    def countdown(self, timeInSeconds, start=True):
        if timeInSeconds == 0:
            self.labelvariable.set("0")
            return
        if start:
            self._starttime = timeInSeconds
        if self._paused:
            self._alarm_id = self.master.after(1000, self.countdown, timeInSeconds, False)
        else:
            hours = timeInSeconds // 3600
            minutes = (timeInSeconds % 3600) // 60
            seconds = timeInSeconds % 60
            time_str = '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
            self.labelvariable.set(time_str)
            self._alarm_id = self.master.after(1000, self.countdown, timeInSeconds-1, False)

if __name__ == '__main__':
    root = Tk()
    root.title("Countdown Timer")
    app = Application(root)
    root.mainloop()
