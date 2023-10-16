import logging
import string
import time
import random

from starlette.middleware.base import BaseHTTPMiddleware

from starlette.requests import Request

logger = logging.getLogger(__name__)


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        logger.info(
            f"rid={idem} start request path={request.url.path}, method={request.method}"
        )
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)
        logger.info(
            f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
        )
        return response
