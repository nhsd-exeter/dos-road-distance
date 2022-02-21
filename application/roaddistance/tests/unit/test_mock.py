import re
import pytest
from common import Common
from traveltime_mock import TravelTimeMock


class TestMock(Common):

    transaction_id: str = "8fcb792e-b914-434d-aa94-b2cb2de25f48"
    STATUS_MSG_COUNT = "Matched on count of "
    STATUS_MSG_TR_ID = "Matched on transaction ID of "
    STATUS_MSG_NONE = "No match, defaulting to "
    STATUS_MSG_NO_SERVICES = "MOCK Matched on count of 0"
    STATUS_MSG_VALUE_OUT_OF_RANGE = "MOCK Matched on value out of range"

    def test_mock_count_5(self):
        r = TravelTimeMock().post(service_count=5)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search(self.STATUS_MSG_COUNT + "5$", r.status_message)

    def test_mock_count_40(self):
        r = TravelTimeMock().post(service_count=40)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search("MOCK From count of 40 using adjusted count of 50$", r.status_message)

    def test_mock_count_3000(self):
        r = TravelTimeMock().post(service_count=3000)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search(self.STATUS_MSG_COUNT + "3000$", r.status_message)

    def test_mock_count_4000(self):
        r = TravelTimeMock().post(service_count=4000)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search(self.STATUS_MSG_NONE + "5$", r.status_message)

    def test_mock_count_0(self):
        r = TravelTimeMock().post(service_count=0)
        print(r.status_code)
        print(r.status_message)
        assert r.status_code == 200
        assert self.STATUS_MSG_NO_SERVICES == r.status_message

    def test_mock_transaction_id(self):
        r = TravelTimeMock().post(transaction_id=self.transaction_id)
        print(self.transaction_id)
        print(r.status_code)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search(self.STATUS_MSG_TR_ID + self.transaction_id, r.status_message)

    def test_mock_no_params(self):
        r = TravelTimeMock().post()
        assert r.status_code == 200
        assert re.search(self.STATUS_MSG_NONE + "5$", r.status_message)

    def test_mock_incorrect_params(self):
        r = TravelTimeMock().post(transaction_id="wrong")
        assert r.status_code == 200
        assert re.search(self.STATUS_MSG_NONE + "5$", r.status_message)


    def test_mock_grid_reference_out_of_range(self):
        invalid_grid_reference_transaction_id: str = "error500_invalid_grid_reference"
        with pytest.raises(ValueError):
            TravelTimeMock().post(transaction_id=invalid_grid_reference_transaction_id)
