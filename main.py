import MusicPlayer
import PartVisualizer
from MusicDownloader import YTMusicDownloader
import neopixel
import board

if __name__ == '__main__':
    led_strip = neopixel.NeoPixel(board.D18, 150, auto_write=False)
    
    v_fft = PartVisualizer.SimpleFFTVisualizer(0,150)
    v_loud = PartVisualizer.LoudVisualizer(65,20)
    v_clear = PartVisualizer.ClearVisualizer(int(150/4),75)
    
    p = MusicPlayer.VisualMusicPlayer("wav_library", [YTMusicDownloader()], led_strip, 150, [v_fft])

    #p.play_song("https://music.youtube.com/watch?v=_dSxAQmrTmQ&feature=shared") #BERGSTEIGEN
    #p.play_song("https://music.youtube.com/watch?v=gymEgOyBaLU&feature=shared") #BHZ Crash Dummy
    #p.play_song("https://www.youtube.com/watch?v=mfLuuur6r8w&pp=ygUQc2VlZWQgYXVnZW5ibGluZw%3D%3D") #augenblng
    #p.play_song("https://www.youtube.com/watch?v=n1nAIIIhT-8&pp=ygULY3Jhc2ggZHVtbXk%3D") #crash dummy
    #p.play_song("https://www.youtube.com/watch?v=60ItHLz5WEA&pp=ygUFZmFkZWQ%3D") #faded alan walker
    #p.play_song("https://www.youtube.com/watch?v=iD__IJWqwY8&pp=ygUbcHJhaXNlIGphaCBpbiB0aGUgbW9vbmxpZ2h0") #praise jah in the moonlight
    #p.play_song("https://www.youtube.com/watch?v=OPf0YbXqDm0&pp=ygUSc3RvcCB3YWl0IGEgbWludXRl")
    #p.play_song("https://www.youtube.com/watch?v=QxA3ULAxyyA&pp=ygUOdmVyemFjaGUgbmVlZHM%3D") #verzache needs
    #p.play_song("https://youtu.be/RML_xJgPpC0?feature=shared")
    #p.play_song("https://www.youtube.com/watch?v=pCPB6WD87Yw&pp=ygUVY2hlaWtoYSByaW1pdHRpIG5vdWFy")
    #p.play_song("https://www.youtube.com/watch?v=d73tiBBzvFM&pp=ygULYWNlIG9mIHBhY2U%3D")
    #p.play_song("https://youtu.be/Xr5gWOD9L4E?feature=shared")
    #p.play_song("https://www.youtube.com/watch?v=xgKWtpVfaWA&pp=ygUWZHIuIGFsYmFuIHdoYXQgaXMgbG92ZQ%3D%3D")
    #p.play_song("youtu.be/dQw4w9WgXcQ") #rick
    #p.play_song("youtu.be/h4UqMyldS7Q")
    #p.play_song("https://youtu.be/AvNRdZjcyp8?si=6MN5b3NbChofxZCf") #Me and I hand in Hand
    #p.play_song("https://music.youtube.com/watch?v=Y3YsRerPcRc&si=ey01yQilYsBzNMkX") # Show me cc
    #p.play_song("https://music.youtube.com/watch?v=uYXFRi63vzM&si=mc-khb3VWdHcHicE") # IN your bones -cc
    p.play_song("https://youtu.be/Hf244LCkkLc?si=sm_RTqya2y4BFlIi") # music sound better wit you
    #p.play_song("https://www.youtube.com/watch?v=TmIwm5RElRs&pp=ygUmaSBkb24ndCB3YW50IHRvIHNldCB0aGUgd29ybGQgb24gZmlyZSA%3D") #
    #p.play_song("https://www.youtube.com/watch?v=WTqnJRIWjVY") # 2 seater (house edit)
    #p.play_song('https://youtu.be/iehmprqF6CQ?si=Csh6KVIR7JwAhL0F') #Crooked Colours Feel Alive
    #p.play_song("https://music.youtube.com/watch?v=nN40K_yHrzk&si=8-E8V4IMiFZ8-si_") # timezones
    #p.play_song("https://music.youtube.com/watch?v=hIjD44WuEBo&si=gFDM8EDMe-vJksWU") #Rosa Rugosa
    #p.play_song("https://www.youtube.com/watch?v=ZEcqHA7dbwM") # fly me to the moon
    #.play_song("https://youtu.be/bkA25uqi66w?si=XJADJA77R8h-JmwK") # sliding doors