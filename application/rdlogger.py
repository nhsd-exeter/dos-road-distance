"""
    Provides a common, bespoke logger abstraction for use by Road Distance

    Typical usage example:

    from rdlogger import RDLogger
    rdlogger = RDLogger()
    rdlogger.log("Put your info log message here")
    rdlogger.log_formatted(request, "ccs_request")
    rdlogger.log_ccs_error("422", "there was an error", <data>)
    rdlogger.log_provider_success("1000001", "no", 1000)
    rdlogger.log_provider_success("1000001", "yes")
    rdlogger.log_provider_error("422", "there was an error", <data>)

    See README for more information including log output formats
"""
import logging
import os
import uuid
import config as config


class RDLogger:

    logger = None
    log_name: str = ""
    log_file_path: str = ""

    # Meters to Miles conversion
    M_TO_MI = 0.000621371

    def __init__(self, log_name: str, request_id: str, transaction_id: str):

        log_config = config.Logging

        if log_name in log_config:
            self.log_name = log_name
            self.log_file_path = log_config[log_name]["Path"]
        else:
            raise ValueError(config.EXCEPTION_LOG_NAME_NOT_FOUND + self.log_name)

        try:
            self.logger = logging.getLogger(__name__ + str(uuid.uuid1().int))
            logging_level = logging.INFO if os.environ.get("DEBUG", "false").lower() == "true" else logging.DEBUG
            self.logger.setLevel(logging_level)

            formatter = logging.Formatter(self.__create_log_format(request_id, transaction_id), "%Y/%m/%d %H:%M:%S")
            self.logger.addHandler(self.__create_stream_handler(formatter))
            self.logger.addHandler(self.__create_file_handler(formatter))
        except Exception as ex:
            print(ex)

    def __create_log_format(self, request_id: str, transaction_id: str) -> str:
        return (
            "%(asctime)s.%(msecs)03d|%(levelname)s|lambda|"
            + request_id
            + "|"
            + transaction_id
            + "|roaddistancepilot|%(message)s"
        )

    def __create_stream_handler(self, formatter):
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        return sh

    def __create_file_handler(self, formatter):
        fh = logging.FileHandler(self.log_file_path)
        fh.setFormatter(formatter)
        return fh

    def format_status(self, log_message: str):
        msg = "system|success|message=" + log_message
        return msg

    def format_ccs_request(self, data: str):
        msg = "ccsrequest|" + data
        return msg

    def format_provider_request(self, data: str):
        msg = "providerrequest|" + data
        return msg

    def format_provider_response(self, data: str):
        msg = "providerresponse|" + data
        return msg

    def format_ccs_request_error(self, errorData: str):
        msg = "|ccsrequest|failed|" + errorData
        return msg

    def format_provider_response_error(self, errorData: str):
        msg = "providerresponse|failed|" + errorData
        return msg

    def read_log_output(self):
        try:
            f = open(self.log_file_path, "r")
            content = f.read()
            f.close()
            return content
        except Exception as ex:
            print(config.EXCEPTION_FILE_CANNOT_BE_OPENED + self.log_file_path + ": ")
            print(ex)

    def purge(self):
        open(self.log_file_path, "w").close()

    def log(self, log_message: str, levelname: str = "info"):
        if levelname == "info":
            self.logger.info(log_message)
        elif levelname == "error":
            self.logger.error(log_message)

    def log_formatted(self, log_message: str, formatter: str, levelname: str = "info"):
        formatterfunc = f"format_{formatter}"
        if hasattr(self, formatterfunc) and callable(func := getattr(self, formatterfunc)):
            self.log(func(log_message), levelname)
        else:
            raise AttributeError(config.EXCEPTION_LOG_FORMATTER_NOT_FOUND + formatter)

    def log_provider_success(self, serviceUid: str, unreachable: str, distance: int = 0):
        if(unreachable == "yes"):
            meters = km = miles = ""
        else:
            meters = str(distance)
            km = str(round(distance/1000, 1))
            miles = str(round(distance * self.M_TO_MI, 1))
        log_message = (
            "success|reference=" + serviceUid + "|unreachable=" + unreachable
            + "|distance=" + meters + "|km=" + km + "|miles=" + miles
        )
        self.log_formatted(log_message, "provider_response")

    def log_provider_error(self, statusCode: str, error: str, data: str = ""):
        log_message = "statuscode=" + statusCode + "|error=" + error + "|data=" + data
        self.log_formatted(log_message, "provider_response_error", "error")

    def log_ccs_error(self, statusCode: str, error: str, data: str = ""):
        log_message = "statuscode=" + statusCode + "|error=" + error + "|data=" + data
        self.log_formatted(log_message, "ccs_request_error", "error")
