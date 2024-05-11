import os
import pygame
import time
import scipy.io.wavfile
import numpy as np

import board
import neopixel

from PartVisualizer import PartVisualizer
from MusicDownloader import MusicDownloader

#-- Class for Playing and Handling Music in a specific Location --"
class MusicPlayer():

    def __init__(self, path, downloader_list: list[MusicDownloader]):
        pygame.mixer.init()
        self.lib_path = os.path.join(os.getcwd(), path)
        self.downloader_list = downloader_list

        for downloader in downloader_list:
             downloader.lib_path = self.lib_path
    
    def get_song(self, url):
        
        download_path = None

        # Probiere alle Download-Anbieter aus
        for downloader in self.downloader_list:
             print("Trying to catch Song with " + str(type(downloader)))
             download_path = downloader.get_song(url)[0]

             if download_path != None:
                  return download_path
        
    
    def play_song(self, url):
         song_path = self.get_song(url)
         pygame.mixer.music.load(song_path)
         pygame.mixer.music.play()

         while(pygame.mixer.music.get_busy()):
              
              position = pygame.mixer.music.get_pos() / 1000.0
              print(f"\rPlaying... {round(position, 1)}",end="")
              time.sleep(0.1)
    
#-- This Class expands the functionality by creating light effects for music --#
class VisualMusicPlayer(MusicPlayer):
    
    def __init__(self, path, downloader_list : list[MusicDownloader],
                 led_strip : neopixel.NeoPixel, led_count : int,
                 visualizer_list : list[PartVisualizer]):
          super().__init__(path, downloader_list)
          
          self.led_strip = led_strip
          self.led_count = led_count
          self.visualizer_list = visualizer_list
          self.part_length = 100 #this variable describes how big the fft-intervall of data in a given moment is


    def play_song(self, url):
        
        self.led_strip.fill((0, 0, 0))
        self.led_strip.show()
        

        song_path = self.get_song(url)
        sample_rate, audio_data = scipy.io.wavfile.read(song_path)

        # get the frequency information about the wav file
        fft_data_all = np.fft.fft(audio_data)
        magnitude_all = np.abs(fft_data_all)
        frequencies_all = np.fft.fftfreq(len(audio_data), 1/sample_rate)
        
        audio_length = len(audio_data)/sample_rate

        max_magnitude = np.max(magnitude_all)

        # Virtual LED Window
        pygame.mixer.pre_init(frequency=sample_rate)
        pygame.mixer.init()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        self.running = True
          
        while pygame.mixer.music.get_busy() and self.running:
            last_pos = 0
            try:
                last_pos = position
            except:
                pass
            position = pygame.mixer.music.get_pos() / 1000
           
            #print(f"\rPlaying... {round(position, 1)}",end="")

            i = int(position * sample_rate) #Calculate which wav-data to use
            passed = position / audio_length
            
            #led_delay = 0 * sample_rate

            start_int = int(max(0,i-self.part_length))
            end_int = int(min(i+self.part_length,audio_length*sample_rate))

            fft_data = np.fft.fft(audio_data[start_int:end_int])
            magnitude_data = np.abs(fft_data)/max_magnitude
           
            for visualizer in self.visualizer_list:
                color_line = visualizer.do_stuff(passed, fft_data, magnitude_data, audio_data)
                
                for i in range(len(color_line)-1, -1, -1):
                    #if color_line[i] != (0,0,0):
                    self.led_strip[visualizer.section_pos+i] = color_line[i]
                self.led_strip.show()
                    
            
            
            #loud = []
            #freq = []
            #w_freq = 0
            #fft_len = 0
            
            #for elem in magnitude_data:
            #    freq.append(elem[0])
            #    loud.append(elem[1])
            #    w_freq += elem[0]*elem[1]
            #    fft_len += 1
            
            #a_loud = np.sum(loud) / fft_len
            #a_freq = w_freq / fft_len
            #max_loud_ind = np.argmax(loud)
            #max_loud_freq = freq[max_loud_ind]
            
            
            #if a_loud > 0.05:
            #    self.led_strip.fill((a_freq*255,255*(1-a_freq),128-(a_freq/2))) #passed*255,max_loud_freq/np.max(frequencies_all)
            #else:
            #    self.led_strip.fill((0, 0, 0)) 
            
            
        
        
        self.led_strip.fill((0, 0, 0))
        self.led_strip.show()
        pygame.quit()


#-- Old and Testing Functions for a Visual Music Player --#
class DeprecatedVisualMusicPlayer(VisualMusicPlayer):
    
     def play_visuals_with_mouse_control(self, url):

          song_path = self.get_song(url)
          sample_rate, audio_data = scipy.io.wavfile.read(song_path)

          # get the frequency information about the wav file
          fft_data_all = np.fft.fft(audio_data)
          magnitude_all = np.abs(fft_data_all)
          frequencies_all = np.fft.fftfreq(len(audio_data), 1/sample_rate)

          audio_length = len(audio_data)/sample_rate

          max_magnitude = np.max(magnitude_all)

          # Virtual LED Window
          pygame.mixer.pre_init(frequency=sample_rate)
          pygame.init()
          self.width, self.height = 1200, 800
          self.screen = pygame.display.set_mode((self.width,self.height))
          pygame.display.set_caption("Simulated LED")
          self.running = True

          pygame.mixer.music.load(song_path)
          pygame.mixer.music.play()
          
          offset_x, offset_y = 0,0


          while pygame.mixer.music.get_busy() and self.running:
               position = pygame.mixer.music.get_pos() / 1000

               i = int(position * sample_rate) #Calculate which wav-data to use
               passed = position / audio_length

               #print(f"Expected {position}, actual {i/sample_rate}, passed {passed*100}%")

               fft_data = np.fft.fft(audio_data[max(0,i):min(i+1,int(audio_length*sample_rate))])
               #fft_data = fft_data_all[max(0,i-1):min(i+2,int(audio_length*sample_rate))]
               magnitude_data = np.abs(fft_data)/max_magnitude

               #print("Curernt Volumes", magnitude_data)

               
               background = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
               background.fill((0,0,0,1))

               self.screen.blit(background, (0,0))

               mouse_pos = pygame.mouse.get_pos()
               invert_x, invert_y = False, False
                            
               # Key Events
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         self.running = False

               keys = pygame.key.get_pressed()
               if keys[pygame.K_LEFT]:
                    offset_x += 2
               if keys[pygame.K_RIGHT]:
                    offset_x -= 2
               if keys[pygame.K_UP]:
                    offset_y += 2
               if keys[pygame.K_DOWN]:
                    offset_y -= 2
               
               if keys[pygame.K_LSHIFT]:
                    invert_x  = True
               if keys[pygame.K_LCTRL]:
                    invert_y  = True

               for i in range(len(fft_data)):
                    freq_pos_x = int(magnitude_data[i][0] * self.width/2)
                    freq_pos_y = int(self.height/2 * (1 - magnitude_data[i][1]*100))

                    #rect = pygame.Rect(freq_pos_x+self.width/2,self.height/2,10,freq_pos_y)
                    
                    #rect = pygame.Rect(offset_x + freq_pos_x+self.width/2,offset_y + freq_pos_y,10,freq_pos_y+self.height/2)
                    #rect2 = pygame.Rect(offset_x + -freq_pos_x+self.width/2,offset_y + freq_pos_y,10,freq_pos_y+self.height/2)
                    
                    #rect = pygame.Rect(offset_x + freq_pos_x+self.width/2,offset_y,10,freq_pos_y)
                    #rect2 = pygame.Rect(offset_x - freq_pos_x+self.width/2,offset_y,10,freq_pos_y)
                    
                    rect = pygame.Rect(offset_x + freq_pos_x+self.width/2,offset_y+freq_pos_y,10,freq_pos_y)
                    rect2 = pygame.Rect(offset_x - freq_pos_x+self.width/2,offset_y+freq_pos_y,10,freq_pos_y)
                    
                    #print(freq_pos_x,freq_pos_y)

                    rect_len = max(0,freq_pos_y / self.height)

                    color = (255*rect_len,255-255*rect_len,128+(rect_len*128))

                    #print(np.abs(self.width/2-freq_pos_x) / self.width)
                    show_rect = [False, False]
                    if invert_x:
                         show_rect[0] = freq_pos_x < np.abs(mouse_pos[0] - self.width/2)
                    else:
                         show_rect[0] = freq_pos_x > np.abs(mouse_pos[0] - self.width/2)
                    
                    if invert_y:
                         show_rect[1] = freq_pos_y < mouse_pos[1]
                    else:
                         show_rect[1] = freq_pos_y > mouse_pos[1]

                    if show_rect[0] and show_rect[1]:
                         pygame.draw.rect(self.screen,color,rect)
                         pygame.draw.rect(self.screen,color,rect2)

               pygame.display.update()
               
          
          pygame.quit()

     def play_visuals(self, url):
          
          song_path = self.get_song(url)
          sample_rate, audio_data = scipy.io.wavfile.read(song_path)

          # get the frequency information about the wav file
          fft_data_all = np.fft.fft(audio_data)
          magnitude_all = np.abs(fft_data_all)
          frequencies_all = np.fft.fftfreq(len(audio_data), 1/sample_rate)

          audio_length = len(audio_data)/sample_rate

          max_magnitude = np.max(magnitude_all)
          
          # Detect the peaks in the audio signal
          #single_audio_data = audio_data
          #if single_audio_data.ndim > 1:
          #     single_audio_data = single_audio_data[:, 0]
          #peaks, _ = signal.find_peaks(single_audio_data)
          # Calculate the time difference between the peaks
          #peak_times = peaks / sample_rate
          #print(np.round(peak_times/60,2))
          #print(f"{np.mean(np.round(np.diff(peak_times),5))}")
          #bpm = 60 / np.mean(np.diff(peak_times))
          #print(f"Estimated BPM: {bpm:.2f}, {peak_times}")
          #return

          # Virtual LED Window
          pygame.mixer.pre_init(frequency=sample_rate)
          pygame.init()
          self.width, self.height = 1200, 800
          self.screen = pygame.display.set_mode((self.width,self.height))
          pygame.display.set_caption("Simulated LED")
          self.running = True

          pygame.mixer.music.load(song_path)
          pygame.mixer.music.play()
          
          offset_x, offset_y = 0,0
          filter = True


          while pygame.mixer.music.get_busy() and self.running:
               last_pos = 0
               try:
                    last_pos = position
               except:
                    pass
               position = pygame.mixer.music.get_pos() / 1000

               i = int(position * sample_rate) #Calculate which wav-data to use
               passed = position / audio_length

               print((position - last_pos) * sample_rate)
               #print(f"Expected {position}, actual {i/sample_rate}, passed {passed*100}%")

               max_size = 400 #(position - last_pos) * sample_rate

               start_int = int(max(0,i-max_size))
               #print(offset_x)
               end_int = int(min(i+max_size,audio_length*sample_rate))

               fft_data = np.fft.fft(audio_data[start_int:end_int])
               #fft_data = fft_data_all
               #fft_data = fft_data_all[max(0,i-1):min(i+2,int(audio_length*sample_rate))]
               magnitude_data = np.abs(fft_data)/max_magnitude

               #print("Curernt Volumes", magnitude_data)

               
               background = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
               background.fill((0,0,0,100))

               self.screen.blit(background, (0,0))

               invert_x, invert_y = False, False
               mouse_pos = pygame.mouse.get_pos()
                            
               # Key Events
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         self.running = False

               keys = pygame.key.get_pressed()
               if keys[pygame.K_LEFT]:
                    offset_x += 2
               if keys[pygame.K_RIGHT]:
                    offset_x -= 2
               if keys[pygame.K_UP]:
                    offset_y += 2
               if keys[pygame.K_DOWN]:
                    offset_y -= 2
               
               if keys[pygame.K_LSHIFT]:
                    invert_x  = True
               if keys[pygame.K_LCTRL]:
                    invert_y  = True
               if keys[pygame.K_f]:
                    filter = False
               else:
                    filter = True


               pos_list = []
               for i in range(len(fft_data)):
                    freq_pos_x = int(magnitude_data[i][0] * self.width/2)
                    freq_pos_y = int(self.height * (magnitude_data[i][1]))

                    #rect = pygame.Rect(freq_pos_x+self.width/2,self.height/2,10,freq_pos_y)
                    
                    #rect = pygame.Rect(offset_x + freq_pos_x+self.width/2,offset_y + freq_pos_y,10,freq_pos_y+self.height/2)
                    #rect2 = pygame.Rect(offset_x + -freq_pos_x+self.width/2,offset_y + freq_pos_y,10,freq_pos_y+self.height/2)
                    
                    #rect = pygame.Rect(offset_x + freq_pos_x+self.width/2,offset_y,10,freq_pos_y)
                    #rect2 = pygame.Rect(offset_x - freq_pos_x+self.width/2,offset_y,10,freq_pos_y)
                    
                    if filter:
                         rect = pygame.Rect(offset_x + freq_pos_x+self.width/2,offset_y+freq_pos_y,10,freq_pos_y)
                         rect2 = pygame.Rect(offset_x - freq_pos_x+self.width/2,offset_y+freq_pos_y,10,freq_pos_y)
                    else:
                         rect = pygame.Rect(offset_x + freq_pos_x+self.width/2,offset_y,10,freq_pos_y)
                         rect2 = pygame.Rect(offset_x - freq_pos_x+self.width/2,offset_y,10,freq_pos_y)     
                    #print(freq_pos_x,freq_pos_y)

                    rect_len = max(0,min(freq_pos_y / self.height,1))
                    pos_list.append(rect_len)
                    #print(rect_len)
                    color = (255*rect_len,255-255*rect_len,128+(rect_len/2*128))

                    #print(np.abs(self.width/2-freq_pos_x) / self.width)
                    show_rect = [False, False]
                    if invert_x:
                         show_rect[0] = freq_pos_x < np.abs(mouse_pos[0] - self.width/2)
                    else:
                         show_rect[0] = freq_pos_x > np.abs(mouse_pos[0] - self.width/2)
                    
                    if invert_y:
                         show_rect[1] = freq_pos_y < mouse_pos[1]
                    else:
                         show_rect[1] = freq_pos_y > mouse_pos[1]
                    
                    if True or show_rect[0] and show_rect[1]:
                         pygame.draw.rect(self.screen,color,rect)
                         pygame.draw.rect(self.screen,color,rect2)

               average = np.sum(pos_list) / len(fft_data) * self.height * 2
               average_rect = pygame.Rect(0,average,self.width,1)
               max_rect = pygame.Rect(0,np.max(pos_list) * self.height * 2,self.width,1)
               pygame.draw.rect(self.screen,(255,0,0),average_rect)
               pygame.draw.rect(self.screen,(0,0,255),max_rect)

               print(average)
               pygame.display.update()
          

          pygame.quit()

     def play_corridor(self, url):

          song_path = self.get_song(url)
          sample_rate, audio_data = scipy.io.wavfile.read(song_path)

          # get the frequency information about the wav file
          fft_data = np.fft.fft(audio_data)
          frequencies = np.fft.fftfreq(len(audio_data), 1/sample_rate)

          audio_length = len(audio_data)/sample_rate


          max_freq = max(frequencies)
          volume_fft = np.abs(fft_data)
          max_volume = volume_fft[0][0]
          for elem in volume_fft:
               for e in elem:
                    if e > max_volume:
                         max_volume = e


          #plt.plot(frequencies, np.abs(fft_data))
          #plt.xlabel('Frequency (Hz)')
          #plt.ylabel('Magnitude')
          #plt.show()

          #bit_depth = np.iinfo(audio_data.dtype).bits
          #print("Bit depth:", bit_depth)


          # Virtual LED Window
          pygame.mixer.pre_init(frequency=sample_rate)
          pygame.init()
          self.width, self.height = 800, 600
          self.screen = pygame.display.set_mode((self.width,self.height))
          pygame.display.set_caption("Simulated LED")
          self.running = True

          pygame.mixer.music.load(song_path)
          pygame.mixer.music.play()


          while pygame.mixer.music.get_busy() and self.running:
               position = pygame.mixer.music.get_pos() / 1000

               i = int(position * sample_rate) #Calculate which wav-data to use
               passed = position / audio_length

               print(f"Expected {position}, actual {i/sample_rate}, passed {passed*100}%")

               fft_data = np.fft.fft(audio_data[max(0,i-1):min(i+2,int(audio_length*sample_rate))])
               volume_data = np.abs(fft_data)



               print(fft_data)

               
               background = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
               background.fill((0,0,0,1))

               self.screen.blit(background, (0,0))

               for i in range(len(fft_data)):
                    freq_pos_x = int(((fft_data[i][0])/max_freq) * self.width/6) + self.width/2
                    freq_pos_y = int(volume_data[i][0])/max_volume * self.height

                    rect_l = pygame.Rect(freq_pos_x,10,10,freq_pos_y)

                    freq_pos_x = int(((fft_data[i][1])/max_freq) * self.width/6) + self.width/2
                    freq_pos_y = int(volume_data[i][1])/max_volume * self.height

                    rect_r = pygame.Rect(freq_pos_x,10,10,freq_pos_y)


                    color = (passed*255,255-255*passed,128+(passed*128))

                    pygame.draw.rect(self.screen,color,rect_l)
                    pygame.draw.rect(self.screen,color,rect_r)

               pygame.display.update()
               

               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         self.running = False
               
          
          pygame.quit()

