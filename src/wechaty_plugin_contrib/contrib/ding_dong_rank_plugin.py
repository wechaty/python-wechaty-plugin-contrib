# """check the weather"""
# from datetime import datetime, timedelta
# import uuid
#
# from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
#
# from wechaty_puppet import get_logger
#
# from wechaty import Message, Wechaty
# from wechaty.plugin import WechatyPlugin
#
#
# log = get_logger('DingDongPluginBot')
#
#
# class DingDongRankPlugin(WechatyPlugin):
#     """weather plugin for bot"""
#
#     def __init__(self):
#         """init the plugin"""
#         super().__init__()
#
#         self.room_data = {}
#         self.interval_time = 8
#         self.clear_seconds = 5
#
#         self.top_k = 10
#         self.room_alias = {}
#
#         self.scheduler = AsyncIOScheduler()
#         self.scheduler.start()
#
#     @property
#     def name(self) -> str:
#         """get the name of the plugin"""
#         return 'ding-dong-rank'
#
#     async def on_message(self, msg: Message):
#         """listen message event"""
#         from_contact = msg.talker()
#         text = msg.text()
#         room = msg.room()
#
#         if room is None:
#             return
#
#         if text in ['#ding', 'dong']:
#             if room.room_id not in self.room_data:
#                 self.room_data[room.room_id] = {
#                     '__status__': 'running'
#                 }
#                 await self.re_init_job(room.room_id)
#         if text == '#ding':
#             self.room_data[room.room_id]['__ding__'] = True
#
#         if text == '#ding start':
#             self.room_data[room.room_id] = {
#                 '__status__': 'running'
#             }
#             await room.say('#ding')
#             await self.re_init_job(room.room_id)
#
#         if text == 'dong':
#             if room.room_id in self.room_data:
#                 if self.room_data[room.room_id]['__status__'] != 'running':
#                     return
#
#                 self.room_data[room.room_id][from_contact.contact_id] = {
#                     'id': from_contact.contact_id,
#                     'time': datetime.now(),
#                     'name': from_contact.name,
#                 }
#                 # refresh the scheduler job
#                 await self.re_init_job(room.room_id)
#
#     async def get_room_alias(self, room_id, member_id, name):
#         """get alias in room
#             this function is not supported in donut wechaty-puppet
#         """
#         room = self.bot.Room(room_id)
#         await room.ready()
#         members = await room.member_all()
#
#         if room_id not in self.room_alias:
#             self.room_alias[room_id] = {}
#             for member in members:
#                 await member.ready()
#                 alias = await room.alias(member)
#                 if alias is None or alias == '':
#                     self.room_alias[room_id][member.contact_id] = \
#                         member.payload.name
#                 else:
#                     self.room_alias[room_id][member.contact_id] = alias
#
#         if member_id not in self.room_alias[room_id]:
#             return name
#         return self.room_alias[room_id][member_id]
#
#     async def send_rank_analysis(self, room_id):
#         """send rank analysis data to conversation room"""
#         log.info('send rank analysis ...')
#         if room_id not in self.room_data:
#             return
#
#         # check if contains ding info
#         if not self.room_data[room_id].get('__ding__', False):
#             return
#
#         bot_ids = [key for key in self.room_data[room_id].keys() if
#                    not key.startswith('__')]
#         dong_data = [self.room_data[room_id][bot_id] for bot_id in bot_ids]
#
#         # sort the date
#         print(dong_data)
#         dong_data.sort(key=lambda x: x['time'])
#
#         top_k_result = []
#         last_timestamp = datetime(year=2000, month=1, day=1)
#         top = 0
#
#         ding_dong_histories = []
#
#         for index, item in enumerate(dong_data):
#
#             if index <= self.top_k:
#                 if item['time'] > last_timestamp:
#                     last_timestamp = item['time']
#                     top += 1
#                 top_k_result.append({
#                     'id': item['id'],
#                     'name': item['name'],
#                     'top': top
#                 })
#                 ding_dong_histories.append(
#                     DingDongHistory(
#                         id=str(uuid.uuid4()),
#                         contact_id=item['id'],
#                         time=item['time'],
#                         room_id=room_id,
#                         rank=top
#                     )
#                 )
#
#         # save history to db
#
#         # send message to the room
#         msg = '🔥🔥 DING-DONG Speed Ranking \n=========================\n'
#
#         icon = {
#             1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣',
#             6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 10: '🔟'
#         }
#
#         for item in top_k_result:
#             if item['top'] in icon:
#                 msg += f'NO.{icon[item["top"]]} {item["name"]}\n'
#
#         room = self.bot.Room.load(room_id)
#         await room.ready()
#         await room.say(msg)
#
#         del self.room_data[room_id]
#
#     def stop_ding_dong_rank(self, room_id: str):
#         """clear all ding-dong history"""
#         log.info('clear ding dong history ...')
#         if room_id in self.room_data:
#             self.room_data[room_id]['__status__'] = 'stopping'
#
#     async def re_init_job(self, room_id):
#         """re init job, replace it if exist"""
#         job_id = f'__job__{room_id}'
#         now = datetime.now()
#
#         # clear all response data in 3 seconds
#         clear_job = self.scheduler.add_job(
#             self.stop_ding_dong_rank,
#             kwargs={'room_id': room_id},
#             id=f'__clear_history__{room_id}',
#             trigger='date',
#             next_run_time=now + timedelta(seconds=self.clear_seconds),
#             replace_existing=True
#         )
#         log.info(clear_job)
#
#         rank_job = self.scheduler.add_job(
#             self.send_rank_analysis,
#             replace_existing=True,
#             id=job_id,
#             trigger='date',
#             next_run_time=now + timedelta(seconds=self.interval_time),
#             kwargs={'room_id': room_id}
#         )
#         log.info(rank_job)
