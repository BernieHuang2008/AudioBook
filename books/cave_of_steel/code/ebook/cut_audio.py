audio_path = "D:/Audible/Download/Isaac Asimov/Robots/[01] The Caves of Steel/The Caves of Steel.mp3"
output_path = "D:/Audible/Download/Isaac Asimov/Robots/[01] The Caves of Steel/part1.mp3"

t_begin = 0
t_end = 2*60*60 + 5*60 + 13  # 2:05:13

import ffmpeg

stream = ffmpeg.input(audio_path, ss=t_begin, to=t_end)
stream = ffmpeg.output(stream, output_path, f="mp3")
ffmpeg.run(stream)
