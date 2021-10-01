import json
from locust import HttpUser, task



class FiveDest(HttpUser):
    weight = 80

    def on_start(self):
        with open('locust/files/ccs_5_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("Test/", data=json.dumps(self.payload), headers=headers)


class FiftyDest(HttpUser):
    weight = 15

    def on_start(self):
        with open('locust/files/ccs_50_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("Test/", data=json.dumps(self.payload), headers=headers)


class FiveHundredDest(HttpUser):
    weight = 3

    def on_start(self):
        with open('locust/files/ccs_500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("Test/", data=json.dumps(self.payload), headers=headers)


class OneThousandFiveHundredDest(HttpUser):
    weight = 1

    def on_start(self):
        with open('locust/files/ccs_1500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("Test/", data=json.dumps(self.payload), headers=headers)


class ThreeThousandDest(HttpUser):
    weight = 1

    def on_start(self):
        with open('locust/files/ccs_3000_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @task
    def do_test(self):
        headers = {'content-type': 'application/json'}
        self.client.post("Test/", data=json.dumps(self.payload), headers=headers)
