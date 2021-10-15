message = "напомни мне 16.10.2021 в 8:00 сходить в школу, завтра"
words = message.split()
date = words[2]
time = words[4]
taskname = " ".join(words[5:])
remind_flag = " ".join(words[:2])
print(remind_flag, date, time, taskname)