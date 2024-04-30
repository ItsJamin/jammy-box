import numpy as np
import sounddevice as sd

def play_and_analyze_music():
    # Set the sample rate and duration
    sample_rate = 44100
    duration = 5  # seconds

    # Generate a sine wave as the audio signal
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    audio_signal = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave

    # Play the audio signal
    sd.play(audio_signal, blocking=True)

    # Analyze the audio signal
    ## Compute the Fast Fourier Transform (FFT)
    fft_signal = np.fft.fft(audio_signal)
    fft_frequencies = np.fft.fftfreq(len(audio_signal), 1/sample_rate)

    ## Find the dominant frequency
    dominant_frequency = fft_frequencies[np.argmax(np.abs(fft_signal))]
    print(f"Dominant frequency: {dominant_frequency:.2f} Hz")

    ## Compute the spectrogram
    spectrogram = np.abs(np.fft.stft(audio_signal, fs=sample_rate))
    print("Spectrogram:")
    print(spectrogram)

if __name__ == "__main__":
    #sd.default.device = "alsa_output.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi___ucm0001.hw_sofhdadsp__sink"
    play_and_analyze_music()