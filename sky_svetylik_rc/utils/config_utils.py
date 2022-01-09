import ujson


class ConfigUtils:
    CONFIG_PATH = 'config/config.json'

    @staticmethod
    def read_value(request_key):
        with open(ConfigUtils.CONFIG_PATH) as fp:
            config = ujson.loads(fp.read())
            return config[request_key]

    @staticmethod
    def write_value(request_key, value):
       return True
