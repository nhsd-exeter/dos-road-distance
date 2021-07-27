import pytest
#from mycode import add
import provider_traveltime

class TestProvider:

	def test_build_url(self):
		pass

	def validate_request(self):
		pass

	def validate_response(self):
		pass

	def test_format_request(self):
		pass

	def test_format_reponse(self):
		pass

	def test_send(self):
		pass

	def test_process_request(self):
		pass

	def test_log(self):
		testLogMessage = 'This is a test log INFO message'

		testLogMessageFormatted = 'road_distance|message="' + testLogMessage + '"'
		provider_traveltime.log(testLogMessage, 'info')
		assert self.logMessage == 'INFO|' + testLogMessageFormatted
		provider_traveltime.log(testLogMessage, 'debug')
		assert self.logMessage == 'DEBUG|' + testLogMessageFormatted
		provider_traveltime.log(testLogMessage, 'error')
		assert self.logMessage == 'ERROR|' + testLogMessageFormatted
