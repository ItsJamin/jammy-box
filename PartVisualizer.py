

#-- This Class is used to dynamically control which parts of the audio is visualized --#
class PartVisualizer():

    def __init__(self, section_begin, section_end, led = None):
        self.led = led
        self.section_begin = section_begin
        self.section_end = section_end
    
    def do_stuff(self, fft_data, magnitude_data, all_audio_data):
        pass
    
    # Convert generated color line to given part of led
    def write_to_led(self):
        if self.led:
            pass
        else:
            pass


class FFTVisualizer(PartVisualizer):

    def do_stuff(self, fft_data, magnitude_data, all_audio_data):

        for i in range(len(fft_data)):
            freq_pos_x = magnitude_data[i][0]
            freq_pos_y = magnitude_data[i][1]
        
        
