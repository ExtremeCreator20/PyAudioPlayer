import os, datetime, random
from logging import info, error, warning, debug, critical, exception, log
import logging
try:
    import audioplayer
except:
    os.system("python -m pip install audioplayer")
    import audioplayer
try:
    import pyttsx3
except:
    os.system("python -m pip install pyttsx3 pywintypes")
    import pyttsx3



musicdir = os.path.expanduser("~/Music")
datadir = os.path.expanduser("~/PyAP")
os.makedirs(musicdir, exist_ok=True)
os.makedirs(datadir, exist_ok=True)



logging.basicConfig(filename=datadir+"\\"+f"player-{datetime.date.today()}.log",level=logging.INFO, filemode="a", format='%(asctime)s - %(levelname)s - %(message)s')
info("Player started")




engine = pyttsx3.init()
engine.setProperty('rate', 125)

def readout(text):
    engine.say(text)
    engine.runAndWait()




def play_audio_files(musicdir, audio_list=None):
    if audio_list is None:
        audio_files = [f for f in os.listdir(musicdir) if f.endswith('.mp3') or f.endswith('.wav')]
    else:
        audio_files = [f for f in audio_list if f.endswith('.mp3') or f.endswith('.wav') and os.path.exists(os.path.join(musicdir, f))]
        auxfr = [f for f in os.listdir(musicdir) if f.endswith('.mp3') or f.endswith('.wav')]
    audionum = 0
    for audio_file in audio_files:
        ls = lister()
        audio_file = ls[audionum]
        #if ls[audionum] != audio_list[audionum]:
        #    warning(f"Audio list file modified from cached, reloading list")
        #    audio_file = ls[audionum]
        if "random" in audio_file.lower():
            adf = audio_file.removesuffix(".mp3").split("-")
            
            if adf[1] == "all":
                random.shuffle(auxfr)
                for auxf in auxfr:
                    info(f"Started playing random audio ({auxf})")
                    file_path = os.path.join(musicdir, auxf)
                    player = audioplayer.AudioPlayer(file_path)
                    player.play(block=True)
                    info(f"Finished playing random audio ({auxf})")
            else:
                auxfs = random.choices(population=auxfr, k=int(adf[1]))
                for auxf in auxfs:
                    info(f"Started playing random audio ({auxf})")
                    file_path = os.path.join(musicdir, auxf)
                    player = audioplayer.AudioPlayer(file_path)
                    player.play(block=True)
                    info(f"Finished playing random audio ({auxf})")
            audionum += 1
            continue
        info(f"Started playing {auxf}")
        file_path = os.path.join(musicdir, audio_file)
        player = audioplayer.AudioPlayer(file_path)
        player.play(block=True)
        info(f"Finished playing {auxf}")
        audionum += 1
        audio_list=ls



def lister():
    file = open(datadir+"\\"+'play.list', 'r')
    audio_list = [line.strip()+".mp3" for line in file.readlines()]
    file.close()
    return audio_list



x = 1
while True:
    play_audio_files(musicdir, lister())
    info(f"Played {x}th loop")
    x+=1