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

        header_values = ""
        if include_headers:
            configured_headers = list(map(lambda header: header.lower(), include_headers.split(",")))
            filtered_dict = {key: value for (key, value) in response.headers.items() if
                             key.lower() in configured_headers}
            if len(filtered_dict) != 0:
                if regex_match is not None:
                    header_values = ".".join(
                        re.search(regex_match, str(value)).group(0) for value in filtered_dict.values())
                else:
                    header_values = ".".join(str(value).replace(".", "_") for value in filtered_dict.values())

        finish = datetime.datetime.now()

        extra = f"{context.request.width}x{context.request.height}{'.' if header_values else '.'}{header_values}" \
            if has_width_and_height else f".{header_values}"

        context.metrics.timing(
            f"original_image_with_size.fetch.{code}.{netloc}.{extra}",
            (finish - req_start).total_seconds() * 1000,
        )
        context.metrics.incr(
            f"original_image_with_size.fetch.{code}.{netloc}.{extra}",
        )

    return http_loader.return_contents(response, url, context, req_start)


async def load(context, url):
    return await http_loader.load(context, url, return_contents_fn=return_contents)
