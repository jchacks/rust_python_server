from locust import HttpUser, between, task


class InvokeUser(HttpUser):
    @task
    def invoke(self):
        self.client.get("/invoke")
