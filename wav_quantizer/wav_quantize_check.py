import numpy as np
import random
import time
import librosa
from tqdm import tqdm
import soundfile as sf
import os


def generate_metronome(wav_file,beat_times):
    metronome,sr = librosa.load('wav_quantizer/metronome.wav',sr=44100)
    metronome2,sr = librosa.load('wav_quantizer/metronomeup.wav', sr=44100)
    original, sr = librosa.load(wav_file, sr=44100)

    metronome = np.array(metronome)
    metronome2 = np.array(metronome2)
    original = np.array(original)
    len_met = len(metronome)

    for i,beat_time in enumerate(beat_times):
        add_timing = int(beat_time * 44100)
        try:
            if i%4==0:
                original[add_timing:add_timing+len_met]+=metronome2
            else:
                original[add_timing:add_timing+len_met]+=metronome
        except:
            pass
    
    sf.write('metronome/'+os.path.basename(wav_file), original, sr)
    return 0
