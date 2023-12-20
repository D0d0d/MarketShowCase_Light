import requests
from app.config import settings
import asyncio


class Verifier:
    inventory_link = settings.INV_LINK
    notification_link = settings.NOTIFICATION_LINK

    def _item(self, id: str, amount: int):
        return {"id": id, "amount": str(amount)}

    def check_item(self, item: dict = _item):
        res = requests.patch(self.link+item["id"]+"/?reserve="+item["amount"])
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(str(res.status_code))

    def notify(self, topic: str = "cons1", text: str = "new order"):
        msg_dict = {"text": text}
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, requests.post, self.notification_link+topic, data=msg_dict)
        # await "result"
