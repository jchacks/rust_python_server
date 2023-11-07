from locust import HttpUser, task


class InvokeUser(HttpUser):
    @task
    def invoke(self):
        self.client.post("/invoke", json={"features": [6.1, 2.8, 4.7, 1.2]})
