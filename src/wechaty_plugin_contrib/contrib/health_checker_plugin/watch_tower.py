# -*- coding: utf-8 -*-


import asyncio
import requests
from typing import List, Optional
import docker
from docker.models.containers import Container
from wechaty_puppet import get_logger


logger = get_logger("WatchTower", file='watch-tower.log')


class WatchTower:

    def __init__(self, name_or_id: str, interval_seconds: int = 60, port: int = 8003) -> None:
        self.name_or_id = name_or_id
        self.interval_seconds = interval_seconds
        self.port = port
        self.retry_times = 5
        
    def find_bot_container(self) -> Optional[Container]:
        client = docker.from_env()
        containers: List[Container] = client.containers.list() or []
        for container in containers:
            if container.name == self.name_or_id or container.id == self.name_or_id:
                return container
        return None

    def check_is_alive(self):
        endpoint = f'http://localhost:{self.port}/ding'
        for index in range(self.retry_times):
            try:
                result = requests.get(endpoint, timeout=60)
                if result is not None and result.json()['msg'] == 'dong':
                    return True
                logger.error(f'retry to check the health of bot {index}/{self.retry_times}....')
            except:
                logger.error(f'retry to check the health of bot {index}/{self.retry_times}....')
                continue
        return False

    async def watch(self):
        logger.info('staring to watch the bot in docker ...')
        while True:
            container = self.find_bot_container()

            if container is not None:
                if not self.check_is_alive():
                    logger.error('===============================================================')
                    logger.error('the bot is not alive. we are trying to restart the container ...')
                    logger.error('===============================================================')
                    container.restart()
                else:
                    logger.info('the bot is alive ...')
            else:
                logger.error('can not find the container of the bot')
            await asyncio.sleep(self.interval_seconds)

if __name__ == '__main__':

    watch_tower = WatchTower(name_or_id='image-of-your-docker', interval_seconds=180)
    asyncio.run(watch_tower.watch())
