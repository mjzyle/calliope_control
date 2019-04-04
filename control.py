# Control module for main GPIO functionality

from time import sleep
import threading
import queue
import timeit
import analysis
import RPi.GPIO as GPIO

# Non-modifiable GPIO pin assignments
pins = (4, 18, 17, 27, 22, 23, 24, 25, 5, 6, 13, 16, 26)

# Playback variables
bpm = 60
pin_offset = 0.0007
song_name = ""
song_last = ""
song_done = 1
qa = queue.Queue()
qb = queue.Queue()
qc = queue.Queue()

# Signals last playback thread to perform analysis of timing data
data_analyzed = 2


# Initialize the GPIO pins
def setup_pins():
    GPIO.setmode(GPIO.BCM)
    for p in pins:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, False)
        print("GPIO Pin " + str(p) + " enabled")


# Clear the GPIO Pins
def clear_pins():
    GPIO.cleanup()
    print("GPIO pins cleared")


# Convert a note into a single GPIO signal (i.e. an array index to a GPIO pin)
def pick_note(arg):
    case = {
        "D1#": 0,
        "E1": 1,
        "F1": 2,
        "F1#": 3,
        "G1": 4,
        "G1#": 5,
        "A2": 6,
        "A2#": 7,
        "B2": 8,
        "C2": 9,
        "C2#": 10,
        "D2": 11,
        "D2#": 12,
        "%": -1
    }
    return case.get(arg)


# Read a formatted text file line by line
def read(filename, q):
    f = open(filename + ".txt", "r")
    song = f.read()

    i = 0
    read_file = 1

    while read_file == 1:
        # Loop to the next note start (notes are separated by spaces)
        while song[i] != "*":
            i = i + 1

        i = i + 1

        # Check if the song is done; if so, exit the loop
        if song[i] == "~":
            read_file = 0
            q.put(-2)

        else:
            # Loop to the note end
            j = i
            while song[j] != " ":
                j = j + 1

            # Write the full note into a temp variable
            note = ""
            while i < j:
                    note = note + song[i]
                    i = i + 1

            # Determine note's corresponding GPIO index from LUT
            out = pick_note(str(note))

            # Add GPIO index to queue
            q.put(out)

    print("Subfile " + filename + " read successfully")
    f.close()


# Read all text files associated with a single song
def read_all(filename):
    global qa, qb, qc
    qa.queue.clear()
    qb.queue.clear()
    qc.queue.clear()

    f = open(filename + ".txt", "r")
    names = f.read()

    i = 0
    j = i
    name = ""
    while names[j] != " ":
        name = name + names[j]
        j = j + 1
    read(name, qa)

    i = j + 1
    j = i
    name = ""
    while names[j] != " ":
        name = name + names[j]
        j = j + 1
    read(name, qb)

    i = j + 1
    j = i
    name = ""
    while names[j] != " ":
        name = name + names[j]
        j = j + 1
    read(name, qc)

    f.close()


# Playback notes one at a time from a single queue
def play(q, id):
    global song_done, bpm, pin_offset

    beat_times = []
    note_times = []
    last_note = -1
    start_beat = timeit.default_timer()
    current_beat = 0

    GPIO.setmode(GPIO.BCM)

    while song_done == 0:
        # Read next note from queue and turn on/off corresponding pins
        sleep(60/bpm)
        note = q.get()
        if note != -2:
            # If last note was not a rest, turn off last pin
            if last_note != -1:
                GPIO.output(pins[last_note], False)
                print("Beat " + str(current_beat)
                      + ": " + str(last_note) + " off")

            # Wait momentarily before turning pins off
            # to account for delay differences
            sleep(pin_offset)

            # Turn on pin only if different from last note
            if last_note != note and note != -1:
                GPIO.output(pins[note], True)
                print("Beat " + str(current_beat)
                      + ": " + str(note) + " on")

            stop_beat = timeit.default_timer()
            beat_times.append(str(stop_beat - start_beat))
            note_times.append(str(stop_beat))

            last_note = note
            start_beat = timeit.default_timer()
            current_beat = current_beat + 1
        else:
            song_done = 1

    # Clear all pins in event that song is ended early
    for p in pins:
        GPIO.output(p, False)
        print(str(p) + " off")

    # Record timing data
    if id == 1:
        f1 = open("beat2beat_A.txt", "w")
        f2 = open("queueA.txt", "w")

    elif id == 2:
        f1 = open("beat2beat_B.txt", "w")
        f2 = open("queueB.txt", "w")

    elif id == 3:
        f1 = open("beat2beat_C.txt", "w")
        f2 = open("queueC.txt", "w")

    for i in beat_times:
        f1.write(i + "\n")

    for i in note_times:
        f2.write(i + "\n")

    f1.close()
    f2.close()


# Play all queues synchronously
def play_all():
    global qa, qb, qc, song_done
    song_done = 0
    thread1 = PlayThread(1, "Player A", qa)
    thread2 = PlayThread(2, "Player B", qb)
    thread3 = PlayThread(3, "Player C", qc)
    thread1.start()
    thread2.start()
    thread3.start()


# Process a song choice
def choose_song(songname):
    global song_last
    read_all(songname)
    song_last = songname
    play_all()


# End a currently playing song early
def stop_song():
    global song_done
    song_done = 1


# Thread to handle playback from a single queue
class PlayThread(threading.Thread):
    def __init__(self, thread_id, name, q):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.q = q

    def run(self):
        global data_analyzed
        print("Starting playback thread " + str(self.thread_id) + "...")
        play(self.q, self.thread_id)
        print("Playback thread " + str(self.thread_id) + " done!")
        if data_analyzed == 0:
            analysis.analyze()
            data_analyzed = 2
            print("Timing data analyzed by thread " + str(self.thread_id))
        else:
            data_analyzed = data_analyzed - 1
