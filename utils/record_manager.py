import json


class RecordManager:
    def readRecord(uid=None):
        with open(
            'record.json',
            'r',
            encoding='utf-8'
        ) as file:
            record = json.load(file)
        
        if uid: return record.get(uid)
        return record

    # def updateAddress(uid, addresses):
    #     record = RecordManager.readRecord(addresses)
        
        