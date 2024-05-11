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
        max_num = 255
        self.color_line[index] = (min(max_num, max(0,self.color_line[index][0] + new_c[0])),
                             min(max_num, max(0,self.color_line[index][1] + new_c[1])),
                             min(max_num, max(0,self.color_line[index][2] + new_c[2])))
    
    def shift_index(self, index, shift, max_ind):
        new_index = int((index + shift) % max_ind)
        return new_index
            
class ClearVisualizer(PartVisualizer):
    
    def do_stuff(self, passed, fft_data, magnitude_data, all_audio_data):
        return self.color_line

class SimpleFFTVisualizer(PartVisualizer):

    def do_stuff(self, passed, fft_data, magnitude_data, all_audio_data):
        
        fading_factor = 8
        
        mid = int(self.section_length / 2)
        
        for j in range(self.section_length):
            dist_to_mid = 1#np.sum(self.color_line[j])/(255*3)#1#(1 - np.abs(mid - j) / (self.section_length / 2))
            
            if dist_to_mid < 0.2:
                dist_to_mid = 0.2
            r = self.color_line[j][0] / 255
            b = self.color_line[j][1] / 255
            g = self.color_line[j][2] / 255
            lim = 0.8
            
            if r > lim:
                r = 1
            else:
                r = lim
            if b > lim:
                b = 1
            else:
                b = lim
            if g > lim:
                g = 1
            else:
                g = lim
            
            
            
            self.add_color(j, (r*-fading_factor*dist_to_mid,
                               b*-fading_factor*dist_to_mid,
                               g*-fading_factor*dist_to_mid))
        
        #self.color_line = [(0,0,0) for _ in range(self.section_length)]
        
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
            freq_pos_x = min(self.section_length-1,int(freq[i]*self.section_length / 2))     
            loudness = loud[i] * (freq[i] + 1.0)
            
            r, b, g = 0, 0, 0
            
            freq_diff = np.abs(max_loud_ind-freq[i]) / (self.section_length / 2)
            #print(loudest_to_passed)
            
            r = a_freq * 128 - (passed * 64 * 16) % 64 #+ (32 + passed * 64 * 16) % 64#self.color_line[mid+freq_pos_x-1][0]#max_loud_freq * 256 #32 + max_loud_freq * 32
            g = 32 * freq_diff - r + (passed * 64 * 8) % 64#self.color_line[freq_pos_x][0] / 2#loudest_to_passed  * 128
            b = 64 - self.color_line[freq_pos_x][1]#256 * loud[max_loud_ind] - self.color_line[freq_pos_x][1]
            
            factor = loudness * 0.2
            r *= factor
            b *= factor
            g *= factor


            #x -= 100
            #z -= 100
            color = (r,g,b)
            #print(mid+freq_pos_x,mid+freq_pos_x)
            #print(color)
            #self.color_line[mid+freq_pos_x] = color
            moving_speed = 100
            shift = g#self.section_length * passed * moving_speed
            pos1 = self.shift_index(mid+freq_pos_x, shift,
                                    self.section_length-1)
            pos2 = self.shift_index(mid-freq_pos_x-1, shift,
                                    self.section_length-1)
            
            self.add_color(pos1, color)
            self.add_color(pos2, color)
            #self.add_color(freq_pos_x, color)
        
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
            
            
