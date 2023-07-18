from wav_quantizer.wav_quantizer import wav_quantizing
from wav_quantizer.wav_quantize_check import generate_metronome
import sys
import os
from music_transcription import transcript

def main():
    wav_folder_name = "test_music"
    wav_filenames = os.listdir(wav_folder_name)
    if sys.argv[1]=='wav_quantize':
        for filename in wav_filenames:
            beat_times = wav_quantizing(os.path.join(wav_folder_name, filename)) # we may save this beat times as metadata for other tasks.
            print("generate_metronome..")
            print(beat_times)
            asdf
            generate_metronome(os.path.join(wav_folder_name, filename),beat_times)
        return 0
    if sys.argv[1]=='source_separation':
        for filename in wav_filenames:
            #os.system("demucs -n mdx_extra "+"\""+ wav_folder_name+"/"+filename+"\"") # 소스가 4개인데 좀 잘함
            os.system("demucs -n htdemucs_6s "+"\""+ wav_folder_name+"/"+filename+"\"") # 6개인데 좀 못함. 가우디오는 6개로 잘하던데.. # 이거도 wav를 별도로 만드는게 아니라 그냥 들여와서 wav로 써야할 것 같은데..


    if sys.argv[1]=='music_transcription':

        mode = "music" #@param ["music-piano", "music-piano-v2", "music-assemble", "chord", "drum", "vocal", "vocal-contour", "beat"]
        transcript(mode, "separated/mdx_extra/Leo Lauretti & Mind Of One - Fight For Us remix/bass.wav") 


    if sys.argv[1]=='chord_transcription':
        mode = "chord"
        transcript(mode, "separated/mdx_extra/Leo Lauretti & Mind Of One - Fight For Us remix/other.wav") 




    if sys.argv[1]=='process_wav':# 이걸 1000번돌리고 잘 저장해두면 similar_metric으로 다다닥 나옴
        """
        
        demucs module을 python 내로 들여서 써야할 수도..
        
        """
        wav = "filename"
        beat_times = wav_quantizing(wav)
        vocal_midi = transcript("vocal", vocal_wav) # 이거 filename으로 불러오는 모듈을 조심스럽게 수정할 필요가 있음.
        bass_midi = transcript("music", bass_wav)
        drum_midi = transcript("drum", drum_wav)
        chord_info = transcript("vocal", other_wav)
        melody_midi = melody_cleanse(transcript("music", other_wav), chord_info) # chord가 이 transcript module에 섞여있긴 해서 고려는 해봐야할 듯.. 이긴 한데 일단은.




        asdf

    if sys.argv[1]=='similar_metric': # wav 1개, 이미 처리되어있는 Library가 있을때 어떤 곡의 어디가 비슷한지
        asdf

if __name__ == '__main__':
    main()