import yaml
import logging

from constants.constants import APP_NAME


class ConfigUtils:

    CONFIG_PATH = '../config/config.yaml'

    def __init__(self):
        self.logger = logging.getLogger(APP_NAME)
        self.logger.setLevel(logging.ERROR)
        pass

    @staticmethod
    def readValue(self, request_key):
        with open(self.CONFIG_PATH, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                for part in data:

                    for key, value in part.items():
                        if request_key == key:
                            return value
                return data
            except yaml.YAMLError as exc:
                self.logger.error(exc)
        return ''
