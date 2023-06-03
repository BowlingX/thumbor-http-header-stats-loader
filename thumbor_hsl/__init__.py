from thumbor.config import Config
import os

Config.define('HSL_REGEX_MATCH_URL', os.environ.get('HSL_REGEX_MATCH_URL'), '', 'HSL')

