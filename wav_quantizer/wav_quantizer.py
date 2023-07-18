import librosa
import scipy.interpolate as interp
import numpy as np
from scipy import stats as st
import madmom, scipy.stats, numpy as np


def wav_quantizing(wav_file, bpm=None):
    """

    Get beat timing of given wav_file. This module assumes wav has integer bpm.

    input : path of wav_file
    output : Beat Timing of given wav file in seconds.
    """
    if bpm==None: #     bpm을 만약 사용자가 넣어주면 사용할 수 있게
        y, sr = librosa.load(wav_file, sr=44100)
        #bpm,beat_times = wav_tracking(y,sr) # or below code, wav_tracking(wav_file) 이 더 빠르고, 아래 5줄 코드가 좀 더 정확하지만 오래걸립니다.
        beats = madmom.features.beats.RNNBeatProcessor()(wav_file)
        beat_times = madmom.features.beats.BeatDetectionProcessor(fps=100)(beats) #CRFBeatDetection, DBNBeatTracking, BeatDetection, BeatTracking 등 Module이 많다.
        m_res = st.linregress(np.arange(len(beat_times)),beat_times)
        bpm = 60/m_res.slope

    int_bpm = round(bpm) # we assume bpm is integer. 
    if abs(int_bpm-bpm)>0.3: #for considering some fast bpm genre(ex. if DnB or future bass genre has 165 bpm, module can compute bpm as 82.5, Note that compute 164bpm song as 82bpm may be ok for beat tracking, but not for 165 bpm.) 
        double_bpm = bpm*2
        int_bpm = round(double_bpm)
    bpm_ratio = round(int_bpm/bpm) # 2 for this implementation
    interpolated_beat_times = interpolate_beat_times(bpm_ratio, int_bpm, beat_times)
    time_shifted = beat_times-interpolated_beat_times[0::bpm_ratio]
    mode_timing = st.mode(np.around(time_shifted,3))
    beat_times = interpolated_beat_times +mode_timing.mode

    while beat_times[0]>60/int_bpm:
        beat_times=beat_times - 60/int_bpm
    if beat_times[0]<0:
        beat_times=beat_times + 60/int_bpm

    while len(y)/44100<beat_times[-1]: # if the beat_time has larger value than full song's length due to shift or something
        beat_times = beat_times[:-1]
    beat_times = beat_times[:-1] #

    print(wav_file,"의 bpm은", bpm,"으로 계산되었습니다.")
    return beat_times

def interpolate_beat_times(bpm_ratio, int_bpm, beat_times):
    beat_steps_8th =  np.linspace(0, beat_times.size*bpm_ratio-1, beat_times.size*bpm_ratio) * (60 / int_bpm)
    return beat_steps_8th


def wav_tracking(wav,sr):
    
    tempo, beats = librosa.beat.beat_track(y=wav, sr=sr)
    beat_times = librosa.frames_to_time(beats,sr=sr)
    time_dif = []
    bpm_in_eachframe=[]
    for i in range(len(beat_times)-1):
        time_dif.append(beat_times[i+1]-beat_times[i])
        bpm_in_eachframe.append(60/(beat_times[i+1]-beat_times[i]))
        print(np.mean(bpm_in_eachframe))
    m_res = st.linregress(np.arange(len(beat_times)),beat_times)
    tempo = 60/m_res.slope

    return tempo, beat_times