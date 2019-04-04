# Helper module for analyzing timing data


# Determine the average beat-to-beat variance for a single engine
def get_avg_b2b(f):
    diffs = []

    times = read_times(f)

    i = 0
    while i < len(times) - 1:
        diffs.append(abs(float(times[i]) - float(times[i + 1])))
        i = i + 1

    avg = 0
    for d in diffs:
        avg = avg + d

    return avg / len(diffs)


# Determine the average differences for two queues playing a sequence of simultaneous beats
def get_avg_q2q(times_1, times_2):
    diffs = []

    i = 0
    while i < len(times_1):
        diffs.append(abs(float(times_1[i]) - float(times_2[i])))
        i = i + 1

    avg = 0
    for d in diffs:
        avg = avg + d

    return avg / len(diffs)


# Read times from a text file into a string list
def read_times(f):
    times = []
    for l in f:
        times.append(str.rstrip(l))
    return times


# Perform bulk analysis and record results to report file
def analyze():
    # Open files
    beat2beat_a = open("beat2beat_A.txt", "r")
    beat2beat_b = open("beat2beat_B.txt", "r")
    beat2beat_c = open("beat2beat_C.txt", "r")
    queue_a = open("queueA.txt", "r")
    queue_b = open("queueB.txt", "r")
    queue_c = open("queueC.txt", "r")
    report = open("report.txt", "w")

    # Perform analysis
    avg_a = get_avg_b2b(beat2beat_a)
    avg_b = get_avg_b2b(beat2beat_b)
    avg_c = get_avg_b2b(beat2beat_c)

    times_a = read_times(queue_a)
    times_b = read_times(queue_b)
    times_c = read_times(queue_c)

    avg_ab = get_avg_q2q(times_a, times_b)
    avg_bc = get_avg_q2q(times_b, times_c)
    avg_ac = get_avg_q2q(times_a, times_c)

    # Print results to report file
    report.write("Average beat-to-beat variances:\n")
    report.write("  Queue A: " + str(avg_a) + " s\n")
    report.write("  Queue B: " + str(avg_b) + " s\n")
    report.write("  Queue C: " + str(avg_c) + " s\n\n")

    report.write("Average queue-to-queue variances:\n")
    report.write("  Queues A and B: " + str(avg_ab) + " s\n")
    report.write("  Queues B and C: " + str(avg_bc) + " s\n")
    report.write("  Queues A and C: " + str(avg_ac) + " s\n")

    # Close files
    beat2beat_a.close()
    beat2beat_b.close()
    beat2beat_c.close()
    queue_a.close()
    queue_b.close()
    queue_c.close()
    report.close()

    print("Timing analysis complete")

