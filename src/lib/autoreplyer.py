import yaml
import logging
import random
import enum

from datetime import datetime, timedelta, timezone
from time import sleep
from typing import NoReturn
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

logging.basicConfig(filename='out/tg_autoreply.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable()

# Aliases
CONFIG_DATA = {str: str | int}
Message = str

class StatusCode(enum.Enum):
    WasConnected = 201
    NowConnected = 202
    Success = 1

class AutoReplyer:
    def __init__(self, config_path: str):
        self.__config: CONFIG_DATA = self._read_config(config_path)
        self.__client = TelegramClient( "tg_session", self.__config["api_id"], self.__config["api_hash"])


    async def _send_message_by_id(self, user_id: int, message=None) -> StatusCode:
        """Send message to telegram account by user id"""
        await self.__client.send_message(user_id, message)
        logging.info("Message has been sent")

        return StatusCode.Success.value


    async def start(self) -> NoReturn:
        await self._sign_in()  # Sign-In to account
        logging.info("Authorization completed")

        while True:
            for user_id in self.__config["user_ids"]:
                await self._messages_handler(user_id)


    async def _messages_handler(self, user_id: int) -> StatusCode:
        message = await self._get_last_message_in_chat(user_id)
        if message.from_id == None and (datetime.utcnow() - message.date.replace(tzinfo=None)) > timedelta(minutes=self.__config["wait"]):  # If difference between current time and send message time, more than 5 minutes, send user a message by user id.
            await self._send_message_by_id(user_id, random.choice(self.__config["messages"]))

        sleep(60)
        return StatusCode.Success.value


    async def _get_last_message_in_chat(self, user_id: int) -> Message:
        return [message async for message in self.__client.iter_messages(user_id)][0]


    async def _sign_in(self) -> StatusCode:
        await self.__client.connect()  # Connect to account
        logging.info("Client connected")

        if await self.__client.is_user_authorized():
            return StatusCode.WasConnected.value  # Check in authorization

        await self.__client.send_code_request(self.__config["phone_number"])  # Send security code
        try:
            await self.__client.sign_in(self.__config["phone_number"], input("Enter a code: "))
        except SessionPasswordNeededError:  # Error throw if enable 2FA
            await self.__client.sign_in(password=self.__config["cloud_password"])  # Sign-In with 2FA password

        return StatusCode.NowConnected.value


    def _read_config(self, config_path: str) -> CONFIG_DATA:
        with open(config_path, "r") as file:
            yaml_config = yaml.safe_load(file)

            return {
                "api_id": yaml_config["application"]["client"]["api_id"],
                "api_hash": yaml_config["application"]["client"]["api_hash"],
                "phone_number": yaml_config["application"]["client"]["phone_number"],
                "cloud_password": yaml_config["application"]["client"]["cloud_password"],
                "user_ids": yaml_config["application"]["user_ids"],
                "messages": yaml_config["application"]["messages"],
                "wait": yaml_config["application"]["time_settings"]["wait"],
            }
