import os,pilk
from pydub import AudioSegment
import datetime

def get_timestmp_string():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def wav2silk(media_path: str, out_path:str='./') -> str:
    media = AudioSegment.from_file(media_path)
    pcm_path = os.path.basename(media_path)
    pcm_path = os.path.splitext(pcm_path)[0]
    silk_path = pcm_path + '.silk'
    pcm_path += '.pcm'
    
    pcm_path = os.path.join(out_path, pcm_path)
    silk_path = os.path.join(out_path, silk_path)
    
    media.export(pcm_path, 's16le', parameters=['-ar', str(media.frame_rate), '-ac', '1']).close()
    duration = pilk.encode(pcm_path, silk_path, pcm_rate=media.frame_rate, tencent=True)
    return silk_path, pcm_path, duration

def silk2pcm(input_silk, out_pcm, pcm_rate = 24000):
    duration = pilk.decode(input_silk, out_pcm, pcm_rate=pcm_rate)
    return duration, out_pcm

def pcm2wav(input_pcm, out_wav, sr):
    cmd = f"ffmpeg -y -f s16le -ar {sr} -ac 1 -i {input_pcm} {out_wav}"
    r = os.system(cmd)
    if r == 0 :
        return True
    else:
        return False

def silk2wav(input_silk,out_wav, sr, out_pcm="temp.pcm"):
    duration = pilk.decode(input_silk, pcm=out_pcm, pcm_rate=sr)
    if pcm2wav(out_pcm, out_wav, sr):
        return out_wav, duration
    else:
        return None    
