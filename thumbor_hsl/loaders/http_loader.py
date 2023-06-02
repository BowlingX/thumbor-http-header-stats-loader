from thumbor.loaders import http_loader
from urllib.parse import urlparse
from thumbor.utils import logger


def return_contents(response, url, context, req_start=None):
    include_headers = context.config.HSL_INCLUDE_HEADERS
    contents = http_loader.return_contents(response, url, context, req_start)

    if include_headers is None:
        logger.warning(
            "[thumbor_hsl]: hsl http loader is enabled, but no headers are configured. Please configure "
            "HSL_INCLUDE_HEADERS")
        return contents

    """Logs additional metrics based on header values"""
    configured_headers = list(map(lambda header: header.lower(), include_headers.split(",")))
    filtered_dict = {key: value for (key, value) in response.headers.items() if key.lower() in configured_headers}

    if len(filtered_dict) == 0:
        return contents

    res = urlparse(url)
    netloc = res.netloc.replace(".", "_")
    code = response.code

    headers = ".".join(str(value).replace(".", "_") for value in filtered_dict.values())

    context.metrics.incr(
        f"original_image_headers.fetch.{code}.{netloc}.{headers}",
    )

    return contents


async def load(context, url):
    return await http_loader.load(context, url, return_contents_fn=return_contents)
