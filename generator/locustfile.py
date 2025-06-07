from locust import HttpUser, task, between

class SurgeUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def surge_endpoint(self):
        self.client.get("/")
