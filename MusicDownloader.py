import os
import yt_dlp

#-- Class for Downloading and Handling Music in a specific Location --"
class MusicDownloader():
     
     def __init__(self, lib_path=None):
          self.lib_path = lib_path
          self.site_marker = ""
     
     def download_song(self, url):
          pass
     
     def extract_music_id(self, url):
          return None
     
     def get_song(self, url): # returns full_path, filename
        video_id = self.extract_music_id(url)
        filename = f"{self.site_marker}{video_id}.wav"
        
        if video_id:
            mp3_filepath = os.path.join(self.lib_path, filename)
            if os.path.exists(mp3_filepath):
                return mp3_filepath, filename
            else:
                 return self.download_song(url), filename

#-- This Class handles YouTube and YouTubeMusic Links --#
class YTMusicDownloader(MusicDownloader):
     
     def __init__(self, lib_path=None):
          super().__init__(lib_path)
          self.site_marker = "yt"
     
     def download_song(self, url):
        
        # Define Options for Downloading
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.lib_path, self.site_marker+'%(id)s.%(ext)s')
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # Extrahiere den Dateinamen der heruntergeladenen Datei
            filename = ydl.prepare_filename(info_dict)

            download_path = os.path.join(self.lib_path,filename)
            
        return os.path.join(self.lib_path, download_path.replace("webm","wav")) 
     
     def extract_music_id(self, url):
        if 'watch?v=' in url:
            video_id = url.split('watch?v=')[1]
        elif 'youtu.be/' in url:
                video_id = url.split('/')[-1]
        else:
                video_id = None
            
        if '&' in video_id:
            video_id = video_id.split('&')[0]
        if '?' in video_id:
            video_id = video_id.split('?')[0]
            
        return video_id
