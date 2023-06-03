from thumbor.config import Config
import os

# The list of headers to include in the stats, separated by ,
Config.define('HSL_INCLUDE_HEADERS', os.environ.get('HSL_INCLUDE_HEADERS'), '', 'HSL')
Config.define('HSL_REGEX_MATCH', os.environ.get('HSL_REGEX_MATCH'), '', 'HSL')

