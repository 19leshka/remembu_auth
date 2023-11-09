import logging
import json


class CustomJSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger_name": record.name,
            "message": record.msg,
        }

        # Access additional fields directly from the record's dictionary
        for key, value in record.__dict__.items():
            if key not in log_data:
                log_data[key] = value

        return json.dumps(log_data, ensure_ascii=False)
