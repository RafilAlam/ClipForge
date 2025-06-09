import os
import ffmpeg
import whisper
import torch
from utils import format_time

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = whisper.load_model('small.en', device=device)
filename = os.listdir('in')[0]

result = model.transcribe(audio='in/' + filename, word_timestamps=True)
segments = result['segments']

srtfile = f"out/{filename.split('.')[0]}.srt"
with open(srtfile, 'w') as f:
    for i, segment in enumerate(segments):
        start_time = format_time(segment['start'])
        end_time = format_time(segment['end'])
        text = segment['text']
        
        f.write(f"{i + 1}\n")
        f.write(f"{start_time} --> {end_time}\n")
        f.write(f"{text}\n\n")

name = filename.split('.')

# Input video
video_input = ffmpeg.input('in/' + filename)
# Burn subtitles into video
video_with_subs = video_input.filter('subtitles', f"out/{name[0]}.srt")
# Input audio (from the same file)
audio_input = ffmpeg.input('in/' + filename).audio

# Combine video with subtitles and original audio
ffmpeg.output(
    video_with_subs,
    audio_input,
    f"out/{name[0]}_subbed.{name[1]}",
    vcodec='libx264',
    acodec='copy',
    strict='experimental'
).overwrite_output().run()