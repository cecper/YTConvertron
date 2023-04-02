from yt_dlp import YoutubeDL
import sys

outputPath = ''
url = ''
format = ''
try:
    url = sys.argv[1]
    format = sys.argv[2]
    outputPath = sys.argv[3]
except IndexError:
    print("Please provide the url, format and output path as arguments.")

#def convert():
    
match format:
    case 'MP3':
        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{outputPath}/%(title)s.mp3',
        'noplaylist': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': 'highest'
        }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        

    case 'lowest quality MP4':

        ydl_opts = {
            'format': 'bestvideo[ext=mp4][height<=480]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': f'{outputPath}/%(title)s.%(ext)s',
            'noplaylist': False
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        

    case 'medium quality MP4':

        ydl_opts = {
            'format': 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': f'{outputPath}/%(title)s.%(ext)s',
            'noplaylist': False
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        
    case 'highest quality MP4':

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{outputPath}/%(title)s.%(ext)s',
            'noplaylist': False
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        

    case 'highest framerate/quality MP4':
        
        ydl_opts = {
            'format': 'bestvideo[fps<=60][ext=mp4]+bestaudio[ext=m4a]/best[fps<=60][ext=mp4]/best',
            'outtmpl': f'{outputPath}/%(title)s.%(ext)s',
            'noplaylist': False
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
