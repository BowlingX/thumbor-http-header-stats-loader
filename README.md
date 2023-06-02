thumbor-http-header-stats-loader
--------------------------------

A modified `http` loader for thumbor which introduces an additional statd counter `original_image_headers.fetch....`

## Configuration

    LOADER="thumbor_hsl.loaders.http_loader"
    HSL_INCLUDE_HEADERS="x-my-header,x-another-header"

This will append the contents of `x-my-header` and `x-another-header` to the
counter `original_image_headers.fetch.{code}.{netloc}.{headers_content_divided_by_dot}`

For example: `original_image_headers.fetch.200.my_source_domain_com.header_value1.header_value2`