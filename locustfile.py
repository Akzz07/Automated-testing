# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2.5) # Waktu tunggu antara permintaan

    host = "http://127.0.0.1:8000" # Ganti dengan alamat server Django Anda

    def on_start(self):
        # Login sebagai user student untuk mendapatkan token
        login_data = {
            "username": "student",
            "password": "password123"
        }
        response = self.client.post("/api/v1/auth/sign-in", json=login_data)
        if response.status_code == 200:
            self.student_token = response.json()['access']
        else:
            print(f"Failed to login: {response.text}")
            self.student_token = None

        # Login sebagai user teacher untuk mendapatkan token
        login_data_teacher = {
            "username": "teacher",
            "password": "password123"
        }
        response_teacher = self.client.post("/api/v1/auth/sign-in", json=login_data_teacher)
        if response_teacher.status_code == 200:
            self.teacher_token = response_teacher.json()['access']
        else:
            print(f"Failed to login as teacher: {response_teacher.text}")
            self.teacher_token = None

        # Buat course jika belum ada (hanya untuk memastikan ada data)
        response_list_courses = self.client.get("/api/v1/courses")
        if response_list_courses.status_code == 200 and len(response_list_courses.json()) == 0:
            if self.teacher_token:
                create_course_data = {
                    "name": "Course for Load Test",
                    "description": "This is a course for load testing",
                    "price": 50
                }
                self.client.post("/api/v1/courses", json=create_course_data,
                                 headers={"Authorization": f"Bearer {self.teacher_token}"})


    @task(3) # Lebih sering diakses
    def list_courses(self):
        self.client.get("/api/v1/courses")

    @task(1) # Lebih jarang diakses
    def enroll_course(self):
        if self.student_token:
            # Asumsi ada course dengan id 1, atau ambil id dari list_courses
            self.client.post("/api/v1/courses/1/enroll",
                             headers={"Authorization": f"Bearer {self.student_token}"})

    @task(1)
    def create_comment(self):
        if self.student_token:
            # Asumsi ada course content dengan id 1, atau buat di on_start
            # Untuk contoh ini, kita asumsikan CourseContent sudah ada
            content_id = 1 # Anda mungkin perlu mengambil ID konten secara dinamis
            comment_data = {"comment": "This is a test comment from load test"}
            self.client.post(f"/api/v1/contents/{content_id}/comments", json=comment_data,
                             headers={"Authorization": f"Bearer {self.student_token}"})