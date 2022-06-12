from locust import HttpUser, task


class Seller(HttpUser):
    @task(1)
    def charge_seller(self):
        self.client.post('/sellers/4/charge/', data={'amount': 1000})

    @task(20)
    def charge_phone(self):
        self.client.post('/sellers/4/charge_phone/', data={'amount': 20, 'phone_number': '09123456789'})
