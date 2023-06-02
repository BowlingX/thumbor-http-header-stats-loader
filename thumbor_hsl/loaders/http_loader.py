import datetime
from thumbor.loaders import http_loader
from urllib.parse import urlparse
from thumbor.utils import logger
import re


def return_contents(response, url, context, req_start=None):
    include_headers = context.config.HSL_INCLUDE_HEADERS
    regex_match = context.config.HSL_REGEX_MATCH

    if include_headers is None:
        logger.warning(
            "[thumbor_hsl]: hsl http loader is enabled, but no headers are configured. Please configure "
            "HSL_INCLUDE_HEADERS")
        return http_loader.return_contents(response, url, context, req_start)

    """Logs additional metrics based on header values"""
    configured_headers = list(map(lambda header: header.lower(), include_headers.split(",")))
    filtered_dict = {key: value for (key, value) in response.headers.items() if key.lower() in configured_headers}

    if len(filtered_dict) == 0:
        return http_loader.return_contents(response, url, context, req_start)

    if req_start:
        res = urlparse(url)
        netloc = res.netloc.replace(".", "_")
        code = response.code

        finish = datetime.datetime.now()

        if regex_match is not None:
            headers = ".".join(re.search(regex_match, str(value)).group(0) for value in filtered_dict.values())
        else:
            headers = ".".join(str(value).replace(".", "_") for value in filtered_dict.values())

        context.metrics.timing(
            f"original_image_headers.fetch.{code}.{netloc}.{headers}",
            (finish - req_start).total_seconds() * 1000,
        )
        context.metrics.incr(
            f"original_image_headers.fetch.{code}.{netloc}.{headers}",
        )

    return http_loader.return_contents(response, url, context, req_start)


async def load(context, url):
    return await http_loader.load(context, url, return_contents_fn=return_contents)
