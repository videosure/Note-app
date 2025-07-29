import tkinter as tk
import shelve


class NoteWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Note Taker")
        self.geometry("400x300")
        self.text = tk.Text(self, wrap="word")
        self.text.pack(fill="both", expand=True)
        self.load_notes()

        # Schedule a call to save_notes every 5 minutes
        self.after(300000, self.auto_save)

    def load_notes(self):
        with shelve.open("notes.db") as db:
            if "text" in db:
                self.text.insert("1.0", db["text"])

    def save_notes(self):
        with shelve.open("notes.db") as db:
            db["text"] = self.text.get("1.0", "end-1c")

    def auto_save(self):
        self.save_notes()
        # Schedule another call to auto_save in 5 minutes
        self.after(300000, self.auto_save)

    def on_close(self):
        self.save_notes()
        self.destroy()

if __name__ == "__main__":
    root = NoteWindow()
    root.protocol("WM_DELETE_WINDOW", root.on_close)
    root.wm_attributes("-topmost", 1) # Make the window topmost
    root.mainloop()
