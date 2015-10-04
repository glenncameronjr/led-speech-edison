import collections
#import mraa
import os
import sys
import time

# Import things for pocketsphinx
import pyaudio
import wave
import pocketsphinx as ps
import sphinxbase

#wemo lib
from ouimeaux.environment import Environment

# Parameters for pocketsphinx
LMD   = "/home/root/led-speech-edison/lm/8484.lm"
DICTD = "/home/root/led-speech-edison/lm/8484.dic"
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2
PATH = 'output'

LED_ON = 1
LED_OFF = 0

#time settings
not_executed = 1

#wemo switch detect
def on_switch(switch):
	print "Switch found!", switch.name
env = Environment(on_switch)
env.start()

#switch = env.get_switch('Bedroom light').on

#switch.explain()
def turn_on():
    switch_on = env.get_switch( 'Bedroom light' ).on()

def turn_off():
    switch_off = env.get_switch( 'Bedroom light' ).off()
    
def decodeSpeech(speech_rec, wav_file):
	wav_file = file(wav_file,'rb')
	wav_file.seek(44)
	speech_rec.decode_raw(wav_file)
	result = speech_rec.get_hyp()
	return result[0]

def main():
    
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
    	
    	dt = list(time.localtime())
        print str(dt[3]) + " : " + str(dt[4]) 
     
        if dt[3] == 14 and dt[4] == 00 and dt[5] >= 00 and dt[5]<=05:
        	os.system('python talking.py')

        # Voice actions
        print recognised 
        if recognised == "LIGHTS ON":
        	turn_on()
        elif recognised == "LIGHTS OFF":
        	turn_off()
        elif recognised == "POWER DOWN":
        	turn_off()
        elif recognised =="VERONICA" or recognised == "VERONIKA":
        	os.system('aplay ~/mic-on.wav')	 
        	
        	
        
    	#cm = 'espeak "'+recognised+'"'
    	#os.system(cm)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Keyboard interrupt received. Cleaning up..."
