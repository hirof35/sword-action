import tkinter as tk
import time

class Stopwatch:
    def __init__(self, window):
        self.window = window
        self.window.title("ストップウォッチ")
        self.window.geometry("300x400")

        self.start_time = 0
        self.elapsed_time = 0
        self.running = False
        self.lap_times = []

        font = ("Helvetica", 24)
        bg_color = "#f0f0f0"
        button_color = "#4CAF50"
        button_text_color = "white"

        self.time_label = tk.Label(text="00:00:00.00", font=("Helvetica", 36), bg=bg_color)
        self.time_label.pack(pady=20)

        self.start_button = tk.Button(text="スタート", command=self.start, font=font, bg=button_color, fg=button_text_color)
        self.start_button.pack(side=tk.TOP, pady=5)

        self.stop_button = tk.Button(text="ストップ", command=self.stop, font=font, bg=button_color, fg=button_text_color)
        self.stop_button.pack(side=tk.TOP, pady=5)

        self.reset_button = tk.Button(text="リセット", command=self.reset, font=font, bg=button_color, fg=button_text_color)
        self.reset_button.pack(side=tk.TOP, pady=5)

        self.lap_button = tk.Button(text="ラップ", command=self.lap, font=font, bg=button_color, fg=button_text_color)
        self.lap_button.pack(side=tk.TOP, pady=5)

        self.lap_label = tk.Label(text="", font=("Helvetica", 12), bg=bg_color)
        self.lap_label.pack(pady=10)

        self.update()

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.update()

    def stop(self):
        if self.running:
            self.running = False

    def reset(self):
        self.elapsed_time = 0
        self.time_label.config(text="00:00:00.00")
        self.lap_times = []
        self.lap_label.config(text="")

    def update(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            if isinstance(self.elapsed_time, (int, float)): # elapsed_timeが数値型であるか確認
                self.time_label.config(text=self.format_time(self.elapsed_time))
        self.window.after(10, self.update)

    def lap(self):
        if self.running:
            lap_time = self.elapsed_time
            self.lap_times.append(lap_time)
            self.display_lap_times()

    def display_lap_times(self):
        lap_text = "ラップタイム:\n"
        for i, lap_time in enumerate(self.lap_times):
            lap_text += f"ラップ{i+1}: {self.format_time(lap_time)}\n"
        self.lap_label.config(text=lap_text)

    def format_time(self, time):
        minutes = int(time / 60)
        seconds = int(time % 60)
        milliseconds = int((time - int(time)) * 100)
        return "{:02d}:{:02d}:{:02d}.{:02d}".format(minutes, seconds, milliseconds, milliseconds % 100 )


window = tk.Tk()
stopwatch = Stopwatch(window)
window.mainloop()
