"""Provides a common, bespoke logger abstraction for use by Road Distance

  Typical usage example:

  from rdlogger import RDLogger
  rdlogger = RDLogger()
  rdlogger.log("Put your info log message here")
  rdlogger.log_formatted(request, "ccs_request")
  rdlogger.log_ccs_error("422", "there was an error")
  rdlogger.log_formatted(request, "provider_request")
  rdlogger.log_formatted(request, "provider_response")
  rdlogger.log_provider_success("1000001", "yes", "1000")
  rdlogger.log_provider_error("422", "there was an error")

  Resultant log formats:
    Basic Log
    YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|roaddistancepilot|<message>
    YYYY/MM/DD 00:00:00.000000+0100|error|lambda|<request_id>|<transaction_id>|roaddistancepilot|<message>

    Status Log - basic status/info (e.g. summary of provider response)
    YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|roaddistancepilot|system|success|message=<message>

    Raw request and response
    YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|roaddistancepilot|ccsrequest|<data>
    YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|roaddistancepilot|providerrequest|<data>
    YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|roaddistancepilot|providerresponse|<data>

    CCS Request Failure
    YYYY/MM/DD 00:00:00.000000+0100|error|lambda|<request_id>|<transaction_id>|roaddistancepilot|ccsrequest|failed|statuscode=<statuscode>|error=<error>

    Provider Response Failure (anything other than 200 response)
    YYYY/MM/DD 00:00:00.000000+0100|error|lambda|<request_id>|<transaction_id>|roaddistancepilot|providerresponse|failed|statuscode=<statuscode>|error=<error>

    Provider Response Success - Per returned service
    YYYY/MM/DD 00:00:00.000000+0100|info|lambda|<request_id>|<transaction_id>|roaddistancepilot|providerresponse|success|reference=<serviceUid>|unreachable=<yes/no>|distance=####
"""
import logging
import sys
import os


class RDLogger:

    logger = None
    log_file_path: str = ""

    def __init__(self, log_file_path: str, request_id: str, transaction_id: str):
        self.log_file_path = log_file_path
        try:
            self.logger = logging.getLogger(__name__)
            logging_level = logging.INFO if os.environ.get("DEBUG", "false").lower() == "true" else logging.DEBUG
            self.logger.setLevel(logging_level)

            sh = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(self.__create_log_format(request_id, transaction_id), "%Y/%m/%d %H:%M:%S")
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)
            self.logger.addHandler(self.__create_file_handler(log_file_path, formatter))
        except Exception as ex:
            print(ex)

    def __create_log_format(self, request_id, transaction_id):
        return (
            "%(asctime)s.%(msecs)03d|%(levelname)s|lambda|"
            + request_id
            + "|"
            + transaction_id
            + "|roaddistancepilot|%(message)s"
        )

    def __create_file_handler(self, log_path: str, formatter):
        fh = logging.FileHandler(log_path)
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
            print("Unable to open file: " + self.log_file_path + ": ")
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
            print("Did not find a function for formatter " + formatter)

    def log_provider_success(self, serviceUid: str, unreachable: str, distance: str = ""):
        log_message = "success|reference=" + serviceUid + "|unreachable=" + unreachable + "|distance=" + distance
        self.log_formatted(log_message, "provider_response")

    def log_provider_error(self, statusCode: str, error: str):
        log_message = "statuscode=" + statusCode + "|error=" + error
        self.log_formatted(log_message, "provider_response_error")

    def log_ccs_error(self, statusCode: str, error: str):
        log_message = "statuscode=" + statusCode + "|error=" + error
        self.log_formatted(log_message, "ccs_request_error")
