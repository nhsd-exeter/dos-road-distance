import task.config as config
from task.common import Common
from traveltime_mock import TravelTimeMock


class TestMock(Common):

    transaction_id: str = "8fcb792e-b914-434d-aa94-b2cb2de25f48"
    request = super().fetch_test_proto_bin(config.PROTO_TRAVEL_TIME_REQUEST_HAPPY_BIN)

    def test_mock_count_5(self):
        self.rdlogger.purge()
        r = TravelTimeMock().post(transaction_id="", service_count=5)
        assert False

    def test_mock_count_3000(self):
        self.rdlogger.purge()
        r = TravelTimeMock().post(transaction_id="", service_count=3000)
        assert False

    def test_mock_transaction_id(self):
        self.rdlogger.purge()
        r = TravelTimeMock().post(transaction_id=self.transaction_id)
        assert False

    def test_mock_no_params(self):
        self.rdlogger.purge()
        r = TravelTimeMock().post(self.request)
        assert False

    def test_mock_incorrect_params(self):
        self.rdlogger.purge()
        r = TravelTimeMock().post(transaction_id="", service_count=1)
        assert False
        r = TravelTimeMock().post(transaction_id="wrong")
        assert False
