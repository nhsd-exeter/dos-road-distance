import re
from task.common import Common
from traveltime_mock import TravelTimeMock


class TestMock(Common):

    transaction_id: str = "8fcb792e-b914-434d-aa94-b2cb2de25f48"

    def test_mock_count_5(self):
        r = TravelTimeMock().post(service_count=5)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search("Matched on count of 5$", r.status_message)

    def test_mock_count_3000(self):
        r = TravelTimeMock().post(service_count=3000)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search("Matched on count of 3000$", r.status_message)

    def test_mock_transaction_id(self):
        r = TravelTimeMock().post(transaction_id=self.transaction_id)
        print(r.status_code)
        assert r.status_code == 200
        print(r.status_message)
        assert re.search(
            "Matched on transaction ID of "
            + self.transaction_id, r.status_message
        )

    def test_mock_no_params(self):
        r = TravelTimeMock().post()
        assert r.status_code == 200
        assert re.search("No match defaulting to 5$", r.status_message)

    def test_mock_incorrect_params(self):
        r = TravelTimeMock().post(service_count=1)
        assert r.status_code == 200
        assert re.search("No match defaulting to 5$", r.status_message)
        r = TravelTimeMock().post(transaction_id="wrong")
        assert r.status_code == 200
        assert re.search("No match defaulting to 5$", r.status_message)
