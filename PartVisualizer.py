import numpy as np

#-- This Class is used to dynamically control which parts of the audio is visualized --#
class PartVisualizer():

    def __init__(self, section_pos, section_length):
        self.section_pos = section_pos
        self.section_length = section_length
        self.color_line = [(0,0,0) for _ in range(self.section_length)]
    
    def do_stuff(self, passed, fft_data, magnitude_data, all_audio_data):
        pass
    
    def add_color(self, index, new_c):
        self.color_line[index] = (min(128, max(0,self.color_line[index][0] + new_c[0])),
                             min(128, max(0,self.color_line[index][1] + new_c[1])),
                             min(128, max(0,self.color_line[index][2] + new_c[2])))
    


class FFTVisualizer(PartVisualizer):

    def do_stuff(self, passed, fft_data, magnitude_data, all_audio_data):
        
        fading_factor = 10
        
        for j in range(self.section_length):
            self.add_color(j, (-fading_factor,-fading_factor,-fading_factor))
        
        #self.color_line = [(0,0,0) for _ in range(self.section_length)]
        
        mid = int(self.section_length / 2) - 1
        
        loud = []
        freq = []
        w_freq = 0
        fft_len = 0
        
        for elem in magnitude_data:
            freq.append(elem[0])
            loud.append(elem[1])
            w_freq += elem[0]*elem[1]
            #print("Loud ", elem[1], "Freq ", elem[0])
            fft_len += 1
            
        a_loud = np.sum(loud) / fft_len
        a_freq = w_freq / fft_len * 4
        a_freq = np.sum(freq) / fft_len * 4
        max_loud_ind = np.argmax(loud)
        max_loud_freq = freq[max_loud_ind]
        
        for i in range(fft_len):
            freq_pos_x = min(self.section_length-1,int(freq[i]* self.section_length/2))
            loudness = loud[i]
            
            r, b, g = 0, 0, 0
            
            loudest_to_passed = min(1,(passed) / np.abs(max_loud_freq-a_freq) * 0.1)
            print(loudest_to_passed)
            
            b = max_loud_freq * 128 #32 + max_loud_freq * 32
            g = 64 + max_loud_freq / 2#a_freq * 10
            r = 64 - max_loud_freq / 2#loudest_to_passed  * 128
            
            if a_freq < 0.3:
                b -= 100
            elif a_freq < 0.6:
                g -= 50
            else:
                r -= 50
            
            factor = 0.1
            r *= factor
            b *= factor
            g *= factor


            #x -= 100
            #z -= 100
            color = (r,b,g)
            #print(mid+freq_pos_x,mid+freq_pos_x)
            #print(color)
            #self.color_line[mid+freq_pos_x] = color
            self.add_color(mid+freq_pos_x, color)
            self.add_color(mid-freq_pos_x, color)
            #self.color_line[mid-freq_pos_x] = color
        
        return self.color_line

class LoudVisualizer(PartVisualizer):
    
        def do_stuff(self, passed, fft_data, magnitude_data, all_audio_data):
        
            fading_factor = 5
            
            for j in range(self.section_length):
                self.add_color(j, (-fading_factor,-fading_factor,-fading_factor))
            mid = int(self.section_length / 2) - 1
            
            loud = []
            freq = []
            w_freq = 0
            fft_len = 0
            
            for elem in magnitude_data:
                freq.append(elem[0])
                loud.append(elem[1])
                w_freq += elem[0]*elem[1]
                #print("Loud ", elem[1], "Freq ", elem[0])
                fft_len += 1
                
            a_loud = np.sum(loud) / fft_len
            a_freq = w_freq / fft_len * 4
            max_loud_ind = np.argmax(loud)
            max_loud_freq = freq[max_loud_ind]
            
            r, b, g = 80, 20, 20
            
            #x -= 100
            #z -= 100
            color = (r,b,g)
            #print(mid+freq_pos_x,mid+freq_pos_x)
            #print(color)
            i=0
            while a_loud > i/self.section_length:
                self.color_line[mid+i] = color
                self.color_line[mid-i] = color
                i += 1
            
            return self.color_line
            
            
