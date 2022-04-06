import re
import pytest
from common import Common
from traveltime_mock import TravelTimeMock


class TestMock(Common):

    transaction_id: str = "8fcb792e-b914-434d-aa94-b2cb2de25f48"
    STATUS_MSG_COUNT = "Matched on count of "
    STATUS_MSG_TR_ID = "Matched on transaction ID of "
    STATUS_MSG_FAILED_TR_ID = "MOCK Failed on transaction ID of "
    STATUS_MSG_ERROR_TR_ID =  "MOCK Matched on error transaction ID of "
    STATUS_MSG_NONE = "No match, defaulting to "
    STATUS_MSG_NO_SERVICES = "MOCK Matched on count of 0"
    STATUS_MSG_VALUE_OUT_OF_RANGE = "MOCK Matched on value out of range"


    def test_mock_count_5(self):
        response = TravelTimeMock().post(service_count=5)
        assert response.status_code == 200
        print(response.status_message)
        assert re.search(self.STATUS_MSG_COUNT + "5$", response.status_message)

    def test_mock_count_40(self):
        response = TravelTimeMock().post(service_count=40)
        assert response.status_code == 200
        print(response.status_message)
        assert re.search("MOCK From count of 40 using adjusted count of 50$", response.status_message)

    def test_mock_count_3000(self):
        response = TravelTimeMock().post(service_count=3000)
        assert response.status_code == 200
        print(response.status_message)
        assert re.search(self.STATUS_MSG_COUNT + "3000$", response.status_message)

    def test_mock_count_4000(self):
        response = TravelTimeMock().post(service_count=4000)
        assert response.status_code == 200
        print(response.status_message)
        assert re.search(self.STATUS_MSG_NONE + "5$", response.status_message)

    def test_mock_count_0(self):
        response = TravelTimeMock().post(service_count=0)
        print(response.status_code)
        print(response.status_message)
        assert response.status_code == 200
        assert self.STATUS_MSG_NO_SERVICES == response.status_message

    def test_mock_transaction_id(self):
        response = TravelTimeMock().post(transaction_id=self.transaction_id)
        print(self.transaction_id)
        print(response.status_code)
        assert response.status_code == 200
        print(response.status_message)
        assert re.search(self.STATUS_MSG_TR_ID + self.transaction_id, response.status_message)

    def test_mock_no_params(self):
        response = TravelTimeMock().post()
        assert response.status_code == 200
        assert re.search(self.STATUS_MSG_NONE + "5$", response.status_message)

    def test_mock_incorrect_params_transaction_id(self):
        response = TravelTimeMock().post(transaction_id="wrong")
        print(response.status_code)
        print(response.status_message)
        assert response.status_code == 200
        assert re.search(self.STATUS_MSG_FAILED_TR_ID + "wrong$", response.status_message)

    def test_mock_incorrect_params_service_count(self):
        response = TravelTimeMock().post(service_count=-2)
        print(response.status_code)
        print(response.status_message)
        assert response.status_code == 200
        assert re.search(self.STATUS_MSG_NONE + "5$", response.status_message)

    def test_mock_incorrect_params_none(self):
        response = TravelTimeMock().post()
        print(response.status_code)
        print(response.status_message)
        assert response.status_code == 200
        assert re.search(self.STATUS_MSG_NONE + "5$", response.status_message)

    def test_mock_grid_reference_out_of_range(self):
        invalid_grid_reference_transaction_id: str = "error500_invalid_grid_reference"
        with pytest.raises(ValueError):
            TravelTimeMock().post(transaction_id=invalid_grid_reference_transaction_id)

    def test_mock_bad_request_sample(self):
        error400_sample: str = "error400_sample"
        response = TravelTimeMock().post(transaction_id=error400_sample)
        print(response.status_code)
        print(response.status_message)
        assert response.status_code == 200
        assert re.search(self.STATUS_MSG_ERROR_TR_ID + "error400_sample$", response.status_message)
