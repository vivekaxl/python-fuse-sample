from collections import OrderedDict
import ConfigParser


class cache():
    def __init__(self, ip, logger, capacity=1000):
        self.ip = ip
        self.logger = logger
        self.aux_folder = self._get_aux_folder()
        self.capacity = capacity
        self.cache = OrderedDict()
        self.filename = self.aux_folder + ip + ".p"

    @staticmethod
    def _get_aux_folder():
        config = ConfigParser.ConfigParser()
        config.read("./config.ini")
        return str(config.get('AUX', 'folder'))

    def set_entry(self, path, method,  data):
        self.logger.debug('cache, set_entry| path: ' + path + ' method: ' + method)
        # Implementing LRU
        if len(self.cache) == self.capacity:
            self.cache.popitem(last=False)
            self.logger.info('Cached: Remove element')

        if path not in self.cache.keys(): self.cache[path] = {}
        if method not in self.cache[path].keys(): self.cache[method] = {}
        self.cache[path][method] = data

    def get_entry(self, path, method):
        try:
            ret_val = self.cache[path][method]
            self.logger.debug('cache, get_entry| path: ' + str(path) + ", method:" + method )
            return ret_val
        except KeyError:
            self.logger.error('cache, get_entry| Entry does not exist| path: ' + str(path) + ", method:" + method)
            return None
