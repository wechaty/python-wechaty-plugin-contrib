from ast import alias
import base64
from urllib import request
from wechaty import WechatyPlugin,get_logger,RoomQueryFilter,ContactQueryFilter,FileBox
from quart import Quart,request
import os
log = get_logger('httpbotplugin')
class httpbotplugin(WechatyPlugin):
    async def blueprint(self, app: Quart) -> None:
        
        @app.get('/send_msg2')
        async def say_hello():
            return 'sucess'
        @app.post('/send_msg')
        async def send_msg():
            item = await request.get_json()
            try:
                msg = get_file_url_str(item.get('msg'),None)
                await send_report(item.get('msg_type'), item.get('name'), msg)
                return '200'
            except Exception as e:
                log.exception(e)
                return 404

        async def send_report(msg_type, name, msg):
            log.info('Bot_' + 'send_report()')
            try:
                if msg_type == 'group_msg':
                    room = await self.bot.Room.find(query = RoomQueryFilter(topic = name))
                    await room.ready()
                    await room.say(msg)
                elif msg_type == 'private_msg':
                    contact = await self.bot.Contact.find(query=ContactQueryFilter(name = name))
                    await contact.say(msg)
                    return '200'
                else:
                    return '0'
            except Exception as e:
                log.exception(e)
        def get_file_url_str(path,base64_code=None):
            if base64_code is None:
                if path.startswith(('http://','https://','HTTP://','HTTPS://')):
                    if path.endswith(('.xls','.xlsx','.pdf','.txt','csv','.doc','.docx','.XLS','.XLSX','.PDF','.TXT','.CSV','.DOC','.DOCX')):
                        #获取url里的文件后缀
                        filename =  os.path.basename(path)
                        #传送网络文件
                        fileBox = FileBox.from_url(path,filename)
                        #fileBox=path+'1'
                    elif path.endswith(('BMP','JPG','JPEG','PNG','GIF','bmp','jpg','jpeg','png','gif')):
                        #传送网络图片
                        fileBox = FileBox.from_url(path,'linshi.jpg')
                        #fileBox=path+'2'
                    else:
                        #传送无后缀的网络图片
                        fileBox = FileBox.from_url(path,'linshi.jpg')
                        #fileBox=path+'3'
                        #发送本地文件
                        #fileBox = FileBox.from_file('/Users/fangjiyuan/Desktop/一组外呼情况汇总.xlsx')
            
                elif path.startswith('/') or path.startswith('\\',2):
                    if path.endswith(('.xls','.xlsx','.pdf','.txt','csv','.doc','.docx','.XLS','.XLSX','.PDF','.TXT','.CSV','.DOC','.DOCX')):
                        #获取本地路径里的文件后缀
                        filename =  os.path.basename(path)
                        #传送本地文件
                        fileBox = FileBox.from_file(path,filename)
                        #fileBox=path+'1'
                    elif path.endswith(('BMP','JPG','JPEG','PNG','GIF','bmp','jpg','jpeg','png','gif')):
                        #传送本地图片
                        fileBox = FileBox.from_file(path,'linshi.jpg')
                        #fileBox=path+'2'
                    elif path.endswith('silk'):
                        fileBox = FileBox.from_file(path,'linshi.silk')
                    elif path.endswith(('MP4','mp4')):
                        fileBox = FileBox.from_file(path,'tmp.mp4')
                    else:
                        #传送本地无后缀的图片
                        fileBox = FileBox.from_file(path,'linshi.jpg')
                else:
                    #发送纯文本
                    fileBox = path
            else:
                fileBox = FileBox.from_base64(base64_code,'linshi.jpg')
            return fileBox