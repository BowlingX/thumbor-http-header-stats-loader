thumbor-http-size-stats-loader
--------------------------------

A modified `http` loader for thumbor which introduces an additional statd
counter `original_image_with_size_fetch.$code.$host.$widthx$height`

## Configuration

    LOADER="thumbor_hsl.loaders.http_loader"