import yaml
import logging

from time import sleep
from typing import NoReturn
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

logging.basicConfig(filename='out/tg_autoreply.log', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
# logging.disable()

CONFIG_DATA = {str: str | int}
Message = str

class AutoReplyer:
    def __init__(self, config_path: str):
        self.__config: CONFIG_DATA = self._read_config(config_path)
        self.__client = TelegramClient( "tg_session", self.__config["api_id"], self.__config["api_hash"])

    async def send_message_by_id(self, user_id: int, message="None"):
        """Send message to telegram account by user id"""
        await self.__client.send_message(user_id, message)
        logging.info("Message has been sent")
        sleep(2)

    async def start(self) -> NoReturn:
        await self.__client.connect()  # Connect to account
        logging.info("Client connected")

        await self._sign_in()  # Sign-In to account
        logging.info("Authorization completed")

        while True:
            for user_id in self.__config["user_ids"]:
                message = await self._get_last_message_in_chat(user_id)
                if message.from_id == None:
                    await self.send_message_by_id(user_id, "**ИДИТЕ НАХУЙ ХОЗЯИН СПИТ!**")
            
            sleep(60 * 5)
            
    async def _get_last_message_in_chat(self, user_id: int) -> Message:
        return [message async for message in self.__client.iter_messages(user_id)][0]

    async def _sign_in(self) -> None:
        if await self.__client.is_user_authorized(): return None  # Check in authorization
        await self.__client.send_code_request(self.phone_number)  # Sent security code

        try:
            await self.__client.sign_in(self.phone_number, input("Enter a code: "))
        except SessionPasswordNeededError:  # Error throw if enable 2FA
            await self.__client.sign_in(password=self.cloud_password)  # Sign-In with 2FA password

    def _read_config(self, config_path: str) -> CONFIG_DATA:
        with open(config_path, "r") as file:
            yaml_config = yaml.safe_load(file)

            return {
                "api_id": yaml_config["client"]["api_id"],
                "api_hash": yaml_config["client"]["api_hash"],
                "phone_number": yaml_config["client"]["phone_number"],
                "cloud_password": yaml_config["client"]["cloud_password"],
                "user_ids": yaml_config["user_ids"]
            }
