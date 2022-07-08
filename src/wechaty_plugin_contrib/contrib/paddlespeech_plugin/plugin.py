import os
from typing import Optional

from wechaty import FileBox, Message, MessageType, WechatyPluginOptions, WechatyPlugin
from wechaty_puppet import get_logger

from paddlespeech.cli.asr.infer import ASRExecutor
from paddlespeech.cli.tts.infer import TTSExecutor
from yaml import dump_all
from .util import wav2silk, silk2wav, get_timestmp_string, silk2pcm


class PaddleSpeechPlugin(WechatyPlugin):
    """PaddleSpeech Plugin"""
    def __init__(self, options: Optional[WechatyPluginOptions] = None):
        super().__init__(options)
        self.cache_dir = f'.wechaty/{self.name}'
        os.makedirs(self.cache_dir, exist_ok=True)
        self.logger = get_logger(self.name, f'{self.cache_dir}/log.log')
        self.asr_model = ASRExecutor()
        self.tts_model = TTSExecutor()
        # first use, download asr & tts model
        self.warm_text = "初始化飞桨语音识别与合成"
        self.warm_path = os.path.join(self.cache_dir, "warm_up.wav")
        self.warm_up()
    
    async def warm_up(self):
        # only chinese
        await self.tts_model(text=self.warm_text, output=self.warm_path) 
        await self.asr_model(self.warm_path, force_yes=True)
    
    async def asr(self, talker:str, input_silk:str) -> str:
        timestmp = get_timestmp_string()
        outwav = os.path.join(self.cache_dir, "asr_" + talker + timestmp  + ".wav")
        outpcm = os.path.join(self.cache_dir, "pcm_" + talker + timestmp + ".pcm")
        trans_result = await silk2wav(input_silk, outwav, sr=16000, out_pcm=outpcm)
        if trans_result:
            out_wav, _ = trans_result
            asr_result = self.asr_model(out_wav, force_yes=True)
        else:
            asr_result = "语音识别错误，音频转换失败"
        return asr_result
    
    def tts(self, talker:str, text) -> str:
        timestmp = get_timestmp_string()
        outwav = os.path.join(self.cache_dir, "tts_" + talker + timestmp  + ".wav")
        self.tts_model(text=text, output=outwav)
        if os.path.exists(outwav):
            outsilk, _, duration = wav2silk(media_path=outwav, out_path=self.cache_dir)
        else:
            outsilk = None
            duration = 0
        return outsilk, duration        
        
    async def on_message(self, msg: Message) -> None:
        """listen message event"""
        if msg.room():
            return
        talker = msg.talker().name
        
        if msg.type() == MessageType.MESSAGE_TYPE_AUDIO:
            # asr
            file_box = await msg.to_file_box()
            saved_file = os.path.join(self.cache_dir, "silk_"+ talker + "_" + get_timestmp_string()+".silk")
            await file_box.to_file(saved_file)
            asr_result = self.asr(talker, saved_file)
            await msg.talker().say(asr_result)
        elif msg.type() == MessageType.MESSAGE_TYPE_TEXT:
            # tts
            text = msg.text()
            outsilk, duration = self.tts(talker, text)
            if outsilk:
                new_audio_file = FileBox.from_file(outsilk)
                new_audio_file.metadata = {
                    "voiceLength": duration * 1000
                }
                await msg.talker().say(new_audio_file)
            else:
                await msg.talker().say("语音合成失败")
            