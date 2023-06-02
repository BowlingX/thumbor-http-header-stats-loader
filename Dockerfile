FROM ghcr.io/minimalcompact/thumbor

RUN pip install tc_aws && pip install https://github.com/BowlingX/thumbor-http-header-stats-loader/archive/main.zip