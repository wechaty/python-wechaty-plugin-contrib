from __future__ import annotations

from quart import Quart
from wechaty import WechatyPlugin, Contact


class HttpBotPlugin(WechatyPlugin):
    async def blueprint(self, app: Quart) -> None:
        @app.route("/api/plugins/http_bot/say/<something>")
        async def say_something(something: str) -> None:
            contact: Contact = self.bot.Contact.load('some-contact-id')
            await contact.say(something)