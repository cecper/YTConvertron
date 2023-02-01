from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg
from pytube import Playlist


def convert(url,format=None,outputPath='.'):

    if not url:
        raise Exception("Please enter a URL.")

    try: 
        match format:
            case 'MP3':
                yt = YouTube(url,on_progress_callback=on_progress)
                yt.streams.get_audio_only().download(output_path=outputPath,filename=f'{yt.title}.mp3')
                return

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
                yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc().first().download(output_path=outputPath,filename="tempVideo.mp4")

                input_video = ffmpeg.input(f'{outputPath}/tempVideo.mp4')
                input_audio = ffmpeg.input(f'{outputPath}/tempAudio.mp3')
                ffmpeg.concat(input_video, input_audio, v=1, a=1).filter('fps', fps=30, round='up').output(f'{outputPath}/{yt.title}1080p.mp4').run()
                return 

            case '1080fps60MP4':
                yt = YouTube(url,on_progress_callback=on_progress)
                yt.streams.filter(abr="160kbps", progressive=False).first().download(output_path=outputPath,filename="tempAudio.mp3")
                yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc().first().download(output_path=outputPath,filename="tempVideo.mp4")
                
                input_video = ffmpeg.input(f'{outputPath}/tempVideo.mp4')
                input_audio = ffmpeg.input(f'{outputPath}/tempAudio.mp3')
                ffmpeg.concat(input_video, input_audio, v=1, a=1).filter('fps', fps=60, round='up').output(f'{outputPath}/{yt.title}1080p.mp4').run()
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
        raise Exception('Your video was not found, check the url. If you\'re trying to download a '
                                           'playlist select the right dropdown item.')
           
            