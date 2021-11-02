import re
from common import Common
from traveltime_mock import TravelTimeMock


class TestMock(Common):

    transaction_id: str = "8fcb792e-b914-434d-aa94-b2cb2de25f48"
    STATUS_MSG_COUNT = "Matched on count of "
    STATUS_MSG_TR_ID = "Matched on transaction ID of "
    STATUS_MSG_NONE = "No match, defaulting to "

    def test_mock_count_5(self):
        r = TravelTimeMock().post(service_count=5)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search(self.STATUS_MSG_COUNT + "5$", r.status_message)

    def test_mock_count_3000(self):
        r = TravelTimeMock().post(service_count=3000)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search(self.STATUS_MSG_COUNT + "3000$", r.status_message)

    def test_mock_transaction_id(self):
        r = TravelTimeMock().post(transaction_id=self.transaction_id)
        print(r.status_code)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search(self.STATUS_MSG_TR_ID + self.transaction_id, r.status_message)

    def test_mock_no_params(self):
        r = TravelTimeMock().post()
        assert r.status_code == 200
        assert re.search(self.STATUS_MSG_NONE + "5$", r.status_message)

    def test_mock_incorrect_params(self):
        r = TravelTimeMock().post(service_count=0)
        assert r.status_code == 200
        assert re.search(self.STATUS_MSG_NONE + "5$", r.status_message)
        r = TravelTimeMock().post(transaction_id="wrong")
        assert r.status_code == 200
        assert re.search(self.STATUS_MSG_NONE + "5$", r.status_message)
