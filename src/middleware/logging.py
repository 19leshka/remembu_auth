import logging
import string
import time
import random
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware

from starlette.requests import Request

from src.core.jsonlogging import CustomJSONFormatter

logger = logging.getLogger(__name__)

logHandler = logging.StreamHandler()
formatter = CustomJSONFormatter()
logHandler.setFormatter(formatter)

logger.addHandler(logHandler)


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S:%f")
        logger.info(
            "Start request",
            extra={
                "time": formatted_time,
                "level": "INFO",
                "rid": idem,
                "start request path": request.url.path,
                "method": request.method,
            },
        )
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)
        logger.info(
            "Request end",
            extra={
                "time": formatted_time,
                "level": "INFO",
                "rid": idem,
                "completed_in": f"{formatted_process_time}ms",
                "status_code": response.status_code,
            },
        )
        return response
