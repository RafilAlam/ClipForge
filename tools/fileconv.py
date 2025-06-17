import os
import ffmpeg

filename = os.listdir('../in')[0]
formatting = input('Output Format: ').lower()

ffmpeg.input('../in/' + filename).output('../out/' + filename.split('.')[0] + '.' + formatting).run()