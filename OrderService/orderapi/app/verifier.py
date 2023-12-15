import requests
from app.config import settings


class Verifier:
    link = settings.INV_LINK

    def _item(self, id: str, amount: int):
        return {"id": id, "amount": str(amount)}

    def check_item(self, item: dict = _item):
        res = requests.patch(self.link+item["id"]+"/?reserve="+item["amount"])
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(str(res.status_code))
