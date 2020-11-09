import yaml
import logging

from constants.constants import APP_NAME


class ConfigUtils:

    CONFIG_PATH = 'config/config.yaml'

    @staticmethod
    def readValue(request_key):
        with open(ConfigUtils.CONFIG_PATH, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                return data[request_key]
            except Exception as exc:
                logging.getLogger(APP_NAME).error(exc)
        return ''
