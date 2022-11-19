from pytube import YouTube
from pytube.cli import on_progress
import moviepy.editor as mpe
import os
def convert(url,format=None,outputPath='.'):
    
    
    yt = YouTube(url,on_progress_callback=on_progress)
    
    
    match format:
        case 'MP3':
            yt.streams.get_audio_only().download(output_path=outputPath,filename=f'{yt.title}.mp3')

        case 'LowMP4':
            yt.streams.get_lowest_resolution().download(output_path=outputPath,filename=f'{yt.title}Low.mp4')

        case '720MP4':
            yt.streams.get_lowest_resolution().download(output_path=outputPath,filename=f'{yt.title}720p.mp4')

        case '1080fps24MP4':
            
            yt.streams.filter(abr="160kbps", progressive=False).first().download(output_path=outputPath,filename="tempAudio.mp3")
            yt.streams.filter(res="1080p", progressive=False).first().download(output_path=outputPath,filename="tempVideo.mp4")

            my_clip = mpe.VideoFileClip(f'{outputPath}/tempVideo.mp4')
            audio_background = mpe.AudioFileClip(f'{outputPath}/tempAudio.mp3')
            final_clip = my_clip.set_audio(audio_background)
            os.chdir(outputPath)
            final_clip.write_videofile(filename=f'{yt.title}1080p.mp4',fps=24)

        case '1080fps60MP4':
            yt.streams.filter(abr="160kbps", progressive=False).first().download(output_path=outputPath,filename="tempAudio.mp3")
            yt.streams.filter(res="1080p", progressive=False).first().download(output_path=outputPath,filename="tempVideo.mp4")

            my_clip = mpe.VideoFileClip(f'{outputPath}/tempVideo.mp4')
            audio_background = mpe.AudioFileClip(f'{outputPath}/tempAudio.mp3')
            final_clip = my_clip.set_audio(audio_background)
            os.chdir(outputPath)
            final_clip.write_videofile(filename=f'{yt.title}1080p.mp4',fps=60)

        case _:
            raise Exception
            
    