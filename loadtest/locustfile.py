from locust import HttpUser, task, between

HOST = "http://localhost:8000"
USER = "admin@gmail.com"
PASS = "admin"

class QuickApiLoad(HttpUser):
    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post("/api/auth/jwt/create", json={"email": USER, "password": PASS})
        if response.status_code == 200:
            json_response_dict = response.json()
            self.token = json_response_dict['access']

    @task
    def index(self):
        headers = {'Authorization': f'JWT {self.token}'}
        self.client.get("/api", headers=headers)