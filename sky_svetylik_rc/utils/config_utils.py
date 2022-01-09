import ujson


class ConfigUtils:
    CONFIG_PATH = 'config/config.json'

    @staticmethod
    def read_value(request_key):
        with open(ConfigUtils.CONFIG_PATH) as fp:
            config = ujson.loads(fp.read())
            print(config[request_key])
            return config[request_key]

    @staticmethod
    def write_value(request_key, value):
       return True
