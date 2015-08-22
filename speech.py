import collections
import mraa
import os
import sys
import time

# Import things for pocketsphinx
import pyaudio
import wave
import pocketsphinx as ps
import sphinxbase


# Parameters for pocketsphinx
LMD   = "/home/root/led-speech-edison/lm/8484.lm"
DICTD = "/home/root/led-speech-edison/lm/8484.dic"
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2
PATH = 'output'

def decodeSpeech(speech_rec, wav_file):
	wav_file = file(wav_file,'rb')
	wav_file.seek(44)
	speech_rec.decode_raw(wav_file)
	result = speech_rec.get_hyp()
	return result[0]

def main():
    # Set direction of LED controls to out
    '''
    for color in leds:
        leds[color].dir(mraa.DIR_OUT)
    '''

    if not os.path.exists(PATH):
        os.makedirs(PATH)

    p = pyaudio.PyAudio()
    speech_rec = ps.Decoder(lm=LMD, dict=DICTD)

    while True:
        # Record audio
    	stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    	print("* recording")
    	frames = []
    	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    		data = stream.read(CHUNK)
    		frames.append(data)
    	print("* done recording")
    	stream.stop_stream()
    	stream.close()
    	#p.terminate()

        # Write .wav file
        fn = "o.wav"
    	wf = wave.open(os.path.join(PATH, fn), 'wb')
    	wf.setnchannels(CHANNELS)
    	wf.setsampwidth(p.get_sample_size(FORMAT))
    	wf.setframerate(RATE)
    	wf.writeframes(b''.join(frames))
    	wf.close()

        # Decode speech
    	wav_file = os.path.join(PATH, fn)
    	recognised = decodeSpeech(speech_rec, wav_file)
    	rec_words = recognised.split()

        # Trigger LEDs
    	#triggerLeds(leds, rec_words)

        # Playback recognized word(s)
    	cm = 'espeak "'+recognised+'"'
        os.system('At your service sir')
    	#os.system(cm)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Keyboard interrupt received. Cleaning up..."
        #allLedsOff(leds)
