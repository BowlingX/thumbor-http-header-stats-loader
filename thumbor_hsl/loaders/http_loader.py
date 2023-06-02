import datetime
from thumbor.loaders import http_loader
from urllib.parse import urlparse


def return_contents(response, url, context, req_start=None):
    if req_start:
        res = urlparse(url)
        netloc = res.netloc.replace(".", "_")
        code = response.code

        finish = datetime.datetime.now()

        if not (context.request.width and context.request.height):
            return http_loader.return_contents(response, url, context, req_start)

        size = f"{context.request.width}x{context.request.height}"

        context.metrics.timing(
            f"original_image_with_size.fetch.{code}.{netloc}.{size}",
            (finish - req_start).total_seconds() * 1000,
        )
        context.metrics.incr(
            f"original_image_with_size.fetch.{code}.{netloc}.{size}",
        )

    return http_loader.return_contents(response, url, context, req_start)


async def load(context, url):
    return await http_loader.load(context, url, return_contents_fn=return_contents)
