import subprocess
import datetime
import forecastio
import unicodedata
import simplejson as json
from urllib2 import Request, urlopen, URLError
import time
import os
from gtts import gTTS
from pydub import AudioSegment

#forecastio api key needed
api_key = "yourAPIkey"
lat = 51.5033630
lng = -0.1276250

forecast = forecastio.load_forecast(api_key, lat, lng)

byHour = forecast.hourly()
hourForecast =  byHour.summary
byCurrent = forecast.currently()

temp = int((byCurrent.temperature * 1.8) + 32)
#print temp

startForecast = "Good morning, its 7am, the temperature in Pacifica is " + str(temp)   + " degrees farenheit. the weather is expected to be " + unicodedata.normalize('NFKD', hourForecast).encode('ascii','ignore')

#print type(hourForecast)
#print type(startForecast)
#print str(datetime.datetime.now())

#/api/county/spots/{county-name}/

request = Request('http://api.spitcast.com/api/spot/forecast/120/')

response = urlopen(request)
kittens = response.read()
parsed_json = json.loads(kittens)
#print parsed_json
spot = parsed_json[1]['spot_name']
swell = parsed_json[1]['size']
#print swell
forecastero = " and The waves at " + str(spot) + " are " + str(swell) + " feet high"

cowskin = startForecast + forecastero

cm = 'espeak "'+cowskin+'"'

#subprocess.call(['say', startForecast])
#subprocess.call(['say', forecastero])

#speech testing on mac
def wake_up():
	os.system(cm)
    #subprocess.call(['say', startForecast])
    #subprocess.call(['say', forecastero])

#wake_up()

def gspeak():
	tts = gTTS(text= cowskin, lang='en-uk')
	tts.save('hello.mp3')
	
	sound = AudioSegment.from_mp3("hello.mp3")
	sound.export("hello.wav", format="wav")
	
	os.system("aplay hello.wav")
	
not_executed = 1

#alarm timer in UTC time
while(not_executed):
    dt = list(time.localtime())
    hour = dt[3]
    minute = dt[4]
    if hour == 18 and minute == 58:
        gspeak()
        not_executed = 0
        while(not_executed == 0):
            if hour == 18 and minute == 59:
            	gspeak()
                #not_executed = 1

not_executed = 0
