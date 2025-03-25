import unittest

# Simple executable class to make sure database unit tests work
class LessonPlanDatabase:
    def __init__(self):
        self.lesson_plans = [] # List containing teacher_id and lesson_plan
    
    # Method to upload lesson plan
    def upload_lesson_plan(self, user_role, teacher_id, lesson_plan):
        if user_role != "teacher":
            return "Access Denied"
        if self is None or user_role is None or teacher_id is None or lesson_plan is None: # Check if any input is null
            return "Missing Information"
        self.lesson_plans.append({"teacher_id": teacher_id, "lesson_plan": lesson_plan}) # Append teacher_id and lesson_plan to lesson_plans list
        return "Lesson Plan Uploaded"
    
    # Method to view lesson plan
    def view_lesson_plans(self, user_role):
        if user_role != "admin":
            return "Access Denied"
        if self is None or user_role is None: # Check if any input is null
            return "Missing Information"
        return self.lesson_plans

# Unit tests for LessonPlanDatabase class
class TestLessonPlanDatabase(unittest.TestCase):
    
    # Set up LessonPlanDatabase object
    def setUp(self):
        self.lesson_plan_db = LessonPlanDatabase()
    
    # Test teacher can upload lesson plan
    def test_teacher_upload_lesson_plan(self):
        response = self.lesson_plan_db.upload_lesson_plan("teacher", "teacher_123", "Lesson 1: Math Basics")
        self.assertEqual(response, "Lesson Plan Uploaded")
        
        uploaded_plans = self.lesson_plan_db.lesson_plans
        self.assertEqual(len(uploaded_plans), 1)
        self.assertEqual(uploaded_plans[0]['teacher_id'], "teacher_123")
        self.assertEqual(uploaded_plans[0]['lesson_plan'], "Lesson 1: Math Basics")
    
    # Test admin can view lesson plans
    def test_admin_view_lesson_plans(self):
        self.lesson_plan_db.upload_lesson_plan("teacher", "teacher_123", "Lesson 1: Math Basics")
        response = self.lesson_plan_db.view_lesson_plans("admin")
        
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['teacher_id'], "teacher_123")
        self.assertEqual(response[0]['lesson_plan'], "Lesson 1: Math Basics")
    
    # Test teacher cannot view lesson plans
    def test_teacher_cannot_view_lesson_plans(self):
        response = self.lesson_plan_db.view_lesson_plans("teacher")
        self.assertEqual(response, "Access Denied")
    
    # Test admin cannot upload lesson plan
    def test_admin_cannot_upload_lesson_plan(self):
        response = self.lesson_plan_db.upload_lesson_plan("admin", "teacher_123", "Lesson 2: Science Basics")
        self.assertEqual(response, "Access Denied")

    # Test null inputs
    def test_null_inputs(self):
        response1 = self.lesson_plan_db.upload_lesson_plan("teacher", None, "Lesson 3: History")
        response2 = self.lesson_plan_db.upload_lesson_plan("teacher", "teacher_123", None)
        response3 = self.lesson_plan_db.upload_lesson_plan("teacher", None, None)
        self.assertEqual(response1, "Missing Information")
        self.assertEqual(response2, "Missing Information")
        self.assertEqual(response3, "Missing Information")
    
if __name__ == "__main__":
    unittest.main()
