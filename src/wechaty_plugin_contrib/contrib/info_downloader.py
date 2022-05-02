"""Download all of the Room/Contact info as a excel file which is exposed as http api"""
import os
from typing import (
    Optional, List
)
from wechaty import (
    WechatyPlugin,
    WechatyPluginOptions,
    Room,
    Contact,
)
from wechaty_puppet import get_logger
import pandas as pd
from quart import Quart, send_file

from wechaty_plugin_contrib.utils import get_invalid_packages

logger = get_logger('InfoDownloaderPlugin', file='.wechaty/info_downloader_plugin.log')


class InfoDownloaderPlugin(WechatyPlugin):
    """Download all of Contacts/Rooms info as excel file

    """

    def __init__(self, options: Optional[WechatyPluginOptions] = None):
        super().__init__(options)

        self.cache_dir = '.wechaty/info_downloader'
        os.makedirs(self.cache_dir, exist_ok=True)

        self._check_dependency_packages()

    # TODO: this feature should be moved to python-wechaty
    def _check_dependency_packages(self):
        """check the dependency packages"""
        packages = ['pandas', 'openpyxl', 'Quart']
        invalid_packages = get_invalid_packages(packages)
        if invalid_packages:
            logger.error(
                'the following packages is not installed, please install them first: %s', invalid_packages
            )
            logger.error('the suggested command: pip install %s', ' '.join(invalid_packages))

    async def get_contacts_infos(self):
        """load all of contact info into csv file format"""
        contacts: List[Contact] = await self.bot.Contact.find_all()
        
        infos = []
        for contact in contacts:
            await contact.ready()
            fields = ['id', 'type', 'name', 'alias', 'friend', 'weixin', 'corporation', 'title', 'description', 'phone']
            info = {}
            for field in fields:
                value = getattr(contact.payload, field) or ''
                info[field] = value
            infos.append(info)
        return infos

    async def get_room_infos(self):
        """load all of room info into csv file format"""
        rooms: List[Room] = await self.bot.Room.find_all()
        
        infos = []
        for room in rooms:
            await room.ready()

            info = {}

            # 1. 初始化群基本信息
            topic = await room.topic()
            topic = topic or room.payload.topic

            info['topic'] = topic
            info['room_id'] = room.room_id

            # 2. 初始化群主信息
            owner = await room.owner()
            info['owner'] = owner.name
            info['owner_id'] = owner.contact_id

            # 3. 初始化群成员信息
            members: List[Contact] = await room.member_list()
            info['member_count'] = len(members)

            infos.append(info)
        
        return infos

    async def blueprint(self, app: Quart) -> None:

        @app.route('/info/download')
        async def info_download():
            # 1. gen the excel file
            contact_infos = await self.get_contacts_infos()
            room_infos = await self.get_room_infos()

            info_file = os.path.join(self.cache_dir, 'wechaty_info.xlsx')
            #create a Pandas Excel writer using XlsxWriter as the engine
            writer = pd.ExcelWriter(info_file, engine='openpyxl')

            pd.DataFrame(contact_infos).to_excel(writer, sheet_name='contacts')
            pd.DataFrame(room_infos).to_excel(writer, sheet_name='rooms')

            writer.save()
            
            # 2. return the file
            response = await send_file(info_file)
            return response