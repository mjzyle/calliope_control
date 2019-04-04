# Main script responsible for processing interface changes and executing
# control processes

import tkinter as tk
import control as c


# Main window frame
class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        #self.configure(borderwidth=250)
        self.pack(padx=10, pady=10)
        c.setup_pins()
        self.main_view()

    # Clear current view before setting up a new window
    # (i.e. destroy all current widgets)
    def clear_view(self):
        for w in self.winfo_children():
            w.destroy()

    # Setup main menu view
    def main_view(self):
        self.clear_view()

        self.comm_line = tk.Label(self,
                                  text="Welcome to our Calliope!",
                                  font=("Helvetica", 15),
                                  fg="blue")
        self.comm_line.pack(side="top")

        self.song_select = tk.Button(self,
                                     text="Choose a song",
                                     font=("Helvetica", 15),
                                     fg="green", command=self.select_view)
        self.song_select.pack(padx=10, pady=10)

        self.song_last = tk.Button(self,
                                   text="Play last song",
                                   font=("Helvetica", 15),
                                   fg="green",
                                   command=self.play_last)
        self.song_last.pack(padx=10, pady=10)

        self.test = tk.Button(self,
                              text="Test engines",
                              font=("Helvetica", 15),
                              fg="orange",
                              command=self.play_test_song)
        self.test.pack(padx=10, pady=10)

        self.debug = tk.Button(self,
                               text="Super secret debugging mode",
                               font=("Helvetica", 5),
                               fg="red",
                               command=self.debug_view)
        self.debug.pack(padx=10, pady=10)

    # Setup select screen view
    def select_view(self):
        self.clear_view()

        self.comm_line = tk.Label(self,
                                  text="Choose a song",
                                  font=("Helvetica", 15),
                                  fg="blue")
        self.comm_line.pack(side="top")

        self.select_almamater = tk.Button(self,
                                          text="Alma Mater (Shine On Forever)",
                                          font=("Helvetica", 15),
                                          fg="green",
                                          command=self.play_alma_mater)
        self.select_almamater.pack(padx=10, pady=10)

        self.select_fightsong = tk.Button(self,
                                          text="Fight Song (Fight On, Case Reserve)",
                                          font=("Helvetica", 15),
                                          fg="green",
                                          command=self.play_fight_song)
        self.select_fightsong.pack(padx=10, pady=10)

        self.select_back = tk.Button(self,
                                     text="BACK",
                                     font=("Helvetica", 15),
                                     fg="red",
                                     command=self.main_view)
        self.select_back.pack(side="bottom")

    # Setup playback screen view
    def play_view(self, song_name, song_case):
        self.clear_view()

        if song_case == 0:
            self.comm_line = tk.Label(self,
                                      text="Playing '" + song_name + "'...",
                                      font=("Helvetica", 15),
                                      fg="blue")
            self.comm_line.pack(side="top", padx=10, pady=10)

        elif song_case == 1:  # Special case for engine test only
            self.comm_line = tk.Label(self,
                                      text=song_name,
                                      font=("Helvetica", 15),
                                      fg="blue")
            self.comm_line.pack(side="top", padx=10, pady=10)

        self.stop_button = tk.Button(self,
                                     text="Home",
                                     font=("Helvetica", 15),
                                     fg="green",
                                     command=self.stop_song)
        self.stop_button.pack(side="bottom")

    # View for accessing on-board OS as a developer
    def debug_view(self):
        self.clear_view()

        self.comm_line = tk.Label(self,
                                  text="WARNING: This feature is intended only for experts and/or people named Matt.",
                                  font=("Helvetica", 15),
                                  fg="red")
        self.comm_line.pack(side="top")

        self.comm_line2 = tk.Label(self,
                                   text="Are you sure you want to continue?",
                                   font=("Helvetica", 15),
                                   fg="red")
        self.comm_line2.pack(padx=10, pady=10)

        self.select_continue = tk.Button(self,
                                         text="Absolutely I do",
                                         font=("Helvetica", 15),
                                         fg="green",
                                         command=self.master.destroy)
        self.select_continue.pack(padx=10, pady=10)

        self.select_back = tk.Button(self,
                                     text="No, take me back",
                                     font=("Helvetica", 15),
                                     fg="green",
                                     command=self.main_view)
        self.select_back.pack(side="bottom")

    # Check if a song has been played when processing "Play last song" command
    def play_last(self):
        if c.song_last != "":
            if c.song_last == "test_song":
                self.play_test_song()
            elif c.song_last == "alma_mater":
                self.play_alma_mater()
            elif c.song_last == "fight_song":
                self.play_fight_song()
        else:
            self.select_view()

    # Load and play alma mater
    def play_alma_mater(self):
        c.choose_song("alma_mater")
        self.play_view("Alma Mater (Shine On Forever)", 0)

    # Load and play fight song
    def play_fight_song(self):
        c.choose_song("fight_song")
        self.play_view("Fight Song (Fight On, Case Reserve)", 0)

    # Load and play engine test
    def play_test_song(self):
        c.choose_song("test_song")
        self.play_view("Testing engines...", 1)

    # End a current playback session
    def stop_song(self):
        c.stop_song()
        self.main_view()


root = tk.Tk()
# root.attributes('-fullscreen', True)

app = MainFrame(master=root)
app.master.title("Calliope")
app.mainloop()

c.clear_pins()
