import yaml
import logging

from constants.constants import APP_NAME


class ConfigUtils:
    CONFIG_PATH = 'config/config.yaml'

    @staticmethod
    def read_value(request_key):
        with open(ConfigUtils.CONFIG_PATH, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                return data[request_key]
            except Exception as exc:
                logging.getLogger(APP_NAME).error(exc)
        return ''

    @staticmethod
    def write_value(request_key, value):
        try:
            data = ''
            with open(ConfigUtils.CONFIG_PATH, 'r') as stream:
                data = yaml.safe_load(stream)

            with open(ConfigUtils.CONFIG_PATH, 'w') as stream:
                data[request_key] = value
                yaml.dump(data, stream)
                return True
        except Exception as exc:
            logging.getLogger(APP_NAME).error(exc)
            return False
