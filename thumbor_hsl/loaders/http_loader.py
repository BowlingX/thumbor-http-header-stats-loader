import datetime
import re
from thumbor.loaders import http_loader
from urllib.parse import urlparse
from thumbor.utils import logger


def return_contents(response, url, context, req_start=None):
    include_headers = context.config.HSL_INCLUDE_HEADERS
    regex_match = context.config.HSL_REGEX_MATCH

    if req_start:
        res = urlparse(url)
        netloc = res.netloc.replace(".", "_")
        code = response.code

        has_width_and_height = bool(context.request.width) and bool(context.request.height)

        if not has_width_and_height and include_headers is None:
            return http_loader.return_contents(response, url, context, req_start)

        extra = ""
        if include_headers:
            configured_headers = list(map(lambda header: header.lower(), include_headers.split(",")))
            filtered_dict = {key: value for (key, value) in response.headers.items() if
                             key.lower() in configured_headers}
            if len(filtered_dict) != 0:
                if regex_match is not None:
                    extra = ".".join(re.search(regex_match, str(value)).group(0) for value in filtered_dict.values())
                else:
                    extra = ".".join(str(value).replace(".", "_") for value in filtered_dict.values())

        finish = datetime.datetime.now()

        size = f"{context.request.width}x{context.request.height}"

        logger.warn(f"original_image_with_size.fetch.{code}.{netloc}.{size}{'.' if extra else ''}{extra}")
        context.metrics.timing(
            f"original_image_with_size.fetch.{code}.{netloc}.{size}{'.' if extra else ''}{extra}",
            (finish - req_start).total_seconds() * 1000,
        )
        context.metrics.incr(
            f"original_image_with_size.fetch.{code}.{netloc}.{size}{'.' if extra else ''}{extra}",
        )

    return http_loader.return_contents(response, url, context, req_start)


async def load(context, url):
    return await http_loader.load(context, url, return_contents_fn=return_contents)
