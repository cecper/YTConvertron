from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg
from pytube import Playlist
import re

def convert(form,url,format=None,outputPath='.'):
    if not url:
        raise Exception("Please enter a URL.")
    
    #Test for playlist in url
    playlist_re = '/playlist\?'
    if(re.search(playlist_re,url)!=None):
            playlist = Playlist(url)
            form.commandLineOut.append(f"Playlist found with title: {playlist.title}")
            print(f"Playlist found with title: {playlist.title}")
            i=0
            for video in playlist.videos:
                i+=1
                try:
                    print(video.title)
                    path = convert_video(form,video.watch_url,format,outputPath)
                    print(f"{video.title} has been downloaded.")
                    return path
                except:
                    print(f"{video.title} could not be downloaded.")
                    form.commandLineOut.append(f"{video.title} could not be downloaded.")
                    pass
    else:
        path = convert_video(form,url,format,outputPath)
        return path
    
def convert_video(form,url,format=None,outputPath='.'):
    try: 
        match format:
            case 'MP3':
                yt = YouTube(url,on_progress_callback=on_progress)
                path = yt.streams.get_audio_only().download(output_path=outputPath,filename=f'{yt.title}.mp3')
                form.commandLineOut.append(f"{yt.title} has been downloaded.")
                return path

            case 'LowMP4':
                yt = YouTube(url,on_progress_callback=on_progress)
                path = yt.streams.get_lowest_resolution().download(output_path=outputPath,filename=f'{yt.title}_low.mp4')
                form.commandLineOut.append(f"{yt.title} has been downloaded.")
                return path

            case '720pMP4':
                yt = YouTube(url,on_progress_callback=on_progress)
                path = yt.streams.get_highest_resolution().download(output_path=outputPath,filename=f'{yt.title}_720p.mp4')
                form.commandLineOut.append(f"{yt.title} has been downloaded.")
                return path
                
            case '1080p30fpsMP4':
                yt = YouTube(url,on_progress_callback=on_progress)
                yt.streams.filter(abr="160kbps", progressive=False).first().download(output_path=outputPath,filename="tempAudio.mp3")
                yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc().first().download(output_path=outputPath,filename="tempVideo.mp4")

                input_video = ffmpeg.input(f'{outputPath}/tempVideo.mp4')
                input_audio = ffmpeg.input(f'{outputPath}/tempAudio.mp3')
                ffmpeg.concat(input_video, input_audio, v=1, a=1).filter('fps', fps=30, round='up').output(f'{outputPath}/{yt.title}_1080p30.mp4').run()
                form.commandLineOut.append(f"{yt.title} has been downloaded.")
                return (f'{outputPath}/{yt.title}_1080p30.mp4')

            case '1080p60fpsMP4':
                yt = YouTube(url,on_progress_callback=on_progress)
                yt.streams.filter(abr="160kbps", progressive=False).first().download(output_path=outputPath,filename="tempAudio.mp3")
                yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc().first().download(output_path=outputPath,filename="tempVideo.mp4")
                
                input_video = ffmpeg.input(f'{outputPath}/tempVideo.mp4')
                input_audio = ffmpeg.input(f'{outputPath}/tempAudio.mp3')
                ffmpeg.concat(input_video, input_audio, v=1, a=1).filter('fps', fps=60, round='up').output(f'{outputPath}/{yt.title}_1080p60.mp4').run()
                form.commandLineOut.append(f"{yt.title} has been downloaded.")
                return (f'{outputPath}/{yt.title}_1080p60.mp4')

    except:
        raise Exception('Your video was not found, check the url.')
