from pytube import YouTube
from pytube.cli import on_progress
import moviepy.editor as mpe
import os
from pytube import Playlist

def convert(url,format=None,outputPath='.'):
    
        
    
    
    try:
        match format:
            case 'MP3':
                yt = YouTube(url,on_progress_callback=on_progress)
                yt.streams.get_audio_only().download(output_path=outputPath,filename=f'{yt.title}.mp3')

            case 'LowMP4':
                yt = YouTube(url,on_progress_callback=on_progress)
                yt.streams.get_lowest_resolution().download(output_path=outputPath,filename=f'{yt.title}Low.mp4')
                return 

            case '720MP4':
                yt = YouTube(url,on_progress_callback=on_progress)
                yt.streams.get_highest_resolution().download(output_path=outputPath,filename=f'{yt.title}720p.mp4')
                return
                
            case '1080fps24MP4':
                yt = YouTube(url,on_progress_callback=on_progress)
                yt.streams.filter(abr="160kbps", progressive=False).first().download(output_path=outputPath,filename="tempAudio.mp3")
                yt.streams.filter(res="1080p", progressive=False).first().download(output_path=outputPath,filename="tempVideo.mp4")

                my_clip = mpe.VideoFileClip(f'{outputPath}/tempVideo.mp4')
                audio_background = mpe.AudioFileClip(f'{outputPath}/tempAudio.mp3')
                final_clip = my_clip.set_audio(audio_background)
                os.chdir(outputPath)
                final_clip.write_videofile(filename=f'{yt.title}1080p.mp4',fps=24)
                return 

            case '1080fps60MP4':
                yt = YouTube(url,on_progress_callback=on_progress)
                yt.streams.filter(abr="160kbps", progressive=False).first().download(output_path=outputPath,filename="tempAudio.mp3")
                yt.streams.filter(res="1080p", progressive=False).first().download(output_path=outputPath,filename="tempVideo.mp4")

                my_clip = mpe.VideoFileClip(f'{outputPath}/tempVideo.mp4')
                audio_background = mpe.AudioFileClip(f'{outputPath}/tempAudio.mp3')
                final_clip = my_clip.set_audio(audio_background)
                os.chdir(outputPath)
                final_clip.write_videofile(filename=f'{yt.title}1080p.mp4',fps=60)
                return 

            case 'playlistMp3':
                playlist = Playlist(url)
                i=0
                for video in playlist.videos:
                    i+=1
                    try:
                        print(video.title)
                        video.streams.get_audio_only().download(output_path=outputPath,filename=f'{i}{video.title}.mp3')
                        print(f"{video.title} has been downloaded.")
                    except:
                        print(f"{video.title} could not be downloaded.")
                        pass

            case 'playlistMp4':
                playlist = Playlist(url)
                i=0
                for video in playlist.videos:
                    i+=1
                    try:
                        print(video.title)
                        video.streams.get_highest_resolution().download(output_path=outputPath,filename=f'{i}{video.title}.mp4')
                    except:
                        print(f"{video.title} could not be downloaded.")
                        pass
                        
    except:
            raise Exception
           
            