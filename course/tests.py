from rest_framework.test import APITestCase
from rest_framework import status


class CourseTestCase(APITestCase):

    def test_course_crud(self):
        resp = self.client.post("/courses/vs/courses", {
            "title": "Maths",
            "description": "Learn maths"
        }, format="json")

        self.assertTrue(resp.status_code == status.HTTP_201_CREATED)

        resp = self.client.get("/courses/vs/courses")
        # print(resp.data)
        self.assertEqual(len(resp.data), 1)

        resp = self.client.patch("/courses/vs/courses/1", {
            "description": "Learn maths change"
        }, format="json")

        self.assertTrue(resp.status_code == status.HTTP_200_OK)

        resp = self.client.get("/courses/vs/courses/1")
        # print(resp.data)

        self.assertEqual(resp.data["description"], "Learn maths change")

        self.client.delete("/courses/vs/courses/1")
        
        resp = self.client.get("/courses/vs/courses")
        print(resp.data)
        self.assertEqual(len(resp.data), 0)
