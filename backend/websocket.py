"""
Handles Websocket messaging
"""
import json
from typing import Any, Dict, List, Tuple

import websockets  # type: ignore
import jwt  # type: ignore

from .models import Message


class WebsocketMessaging:
    users: Dict[str, Any]
    secret: str
    session: Any

    def __init__(self, secret: str, session: Any):
        self.users = {}
        self.secret = secret
        self.session = session

    async def register_user(self, handle: str, websocket: Any) -> None:
        """
        Registers a User as online

        Parameters
        ----------

        handle: str
            User handle

        websocket: Any
            Socket used to communicate with user
        """
        self.users[handle] = websocket

    async def unregister_user(self, handle: str) -> None:
        """
        Unregisters a User

        Parameters
        ----------

        handle: str
             User to register
        """
        del self.users[handle]

    @staticmethod
    def _parse_path(path: str) -> Tuple[str, str]:
        """
        Parses a URL Extension Path

        Parameters
        ----------

        path: str
            URL Extension
            Should be form of /<handle>/<token>
        """
        values: List[str] = path.split("/")
        if len(values) != 3:
            return ("", "")
        return (values[1], values[2])

    async def send_message(self, message: Message) -> None:
        """
        Attempts to send the message to the reciever

        If the reciever is not in self.users do nothing

        Parameters
        ----------

        msg: Dict[str, str]
            Message Data
        """
        if message.reciever not in self.users:
            return
        self.users[message.reciever].send(message.to_reciever_json())

    async def start(self, websocket, path: str) -> None:
        """
        Main entry point to WebsocketMessaging

        Sends messages in realtime, iff both users are connected, if reciever is not connected
        This will just save the message for the user for later.

        parameters
        ----------

        websocket: websockets.WebsocketServerProtocol
             Socket used to communicate back and forth with user

        path: str
             URL Extension
             should be /<handle>/<token>

        Expected Message
        ----------------

        {
          "sender": $sender_handle,
          "reciever": $reciever_handle,
          "reciever_message": $reciever_message,
          "sender_message": $sender_message
        }

        Sent Messages
        -------------

        {
         "sender": $sender_handle,
         "reciever_message": $reciever_message,
         "date": $date
        }
        """
        (handle, token) = self._parse_path(path)
        if not handle or not token:
            return
        try:
            jwt.decode(token, self.secret, algorithms=["HS256"])
        except jwt.DecodeError:
            return
        await self.register_user(handle, websocket)
        try:
            async for message in websocket:
                msg = await websocket.recv()
                data = json.loads(msg)
                message = Message(**data)
                print(message)
                self.session.add(message)
                self.session.commit()
                await self.send_message(message)
        finally:
            await self.unregister_user(handle)
