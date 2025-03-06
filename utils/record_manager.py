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

    def updateRecord(uid, new_record):
        record = RecordManager.readRecord();
        record[uid] = new_record

        with open(
            'record.json',
            'w',
            encoding='utf-8',
        ) as file:
            json.dump(
                record,
                file,
                ensure_ascii=False,
                indent=4
            )
        
    