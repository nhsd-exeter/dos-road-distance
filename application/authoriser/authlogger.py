import logging
import uuid


class AuthLogger:
    logger = None

    def __init__(self):
        try:
            self.logger = logging.getLogger(__name__ + str(uuid.uuid1().int))
            self.logger.setLevel(logging.DEBUG)
            self.logger.propagate = False

            formatter = logging.Formatter(self.__create_log_format(), "%Y/%m/%d %H:%M:%S")
            self.logger.addHandler(self.__create_stream_handler(formatter))
        except Exception as ex:
            print(ex)

    def __create_log_format(self) -> str:
        return "%(asctime)s.%(msecs)03d|%(levelname)s|lambda|||road_distance_authorizer|%(message)s"

    def __create_stream_handler(self, formatter):
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        return sh

    def log(self, log_message: str, levelname: str = "info"):
        if levelname == "info":
            self.logger.info(log_message)
        elif levelname == "error":
            self.logger.error(log_message)
