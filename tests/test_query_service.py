import unittest
from unittest.mock import MagicMock
from query_service import QueryService
from data_access import DBManager



class TestQueryService(unittest.TestCase):

    def setUp(self):
        self.db_mock = MagicMock(DBManager)
        self.service = QueryService(self.db_mock)


    def test_get_students_count_by_room_success(self):
        output= [("Room A", 20), ("Room B", 30)]

        self.db_mock.execute_analysis_query.return_value= (True, output, 2)

        result = self.service.get_students_count_by_room()
        
        self.assertEqual(result, output)

        self.db_mock.execute_analysis_query.assert_called_once()

    def test_get_students_count_by_room_failed(self):
        
        self.db_mock.execute_analysis_query.return_value= (False, None, 0)

        result = self.service.get_students_count_by_room()
        
        self.assertIsNone(result)


    def test_get_rooms_by_smallest_age_avg_success(self):
        output=[("Room A", 3),("Room B", 5)]

        self.db_mock.execute_analysis_query.return_value= (True, output, 2)

        result = self.service.get_rooms_by_smallest_age_avg()
        
        self.assertEqual(result, output)
        self.db_mock.execute_analysis_query.assert_called_once()

    def test_get_rooms_by_smallest_age_avg_failed(self):

        self.db_mock.execute_analysis_query.return_value= (False, None, 0)
        result = self.service.get_rooms_by_smallest_age_avg()
        self.assertIsNone(result)


    def test_get_rooms_by_largest_def_age_success(self):
        output=[("Room A", 6),("Room B", 7)]

        self.db_mock.execute_analysis_query.return_value= (True, output, 2)

        result = self.service.get_rooms_by_largest_def_age()
        
        self.assertEqual(result, output)
        self.db_mock.execute_analysis_query.assert_called_once()

    def test_get_rooms_by_largest_def_age_failed(self):

        self.db_mock.execute_analysis_query.return_value= (False, None, 0)
        result = self.service.get_rooms_by_largest_def_age()
        self.assertIsNone(result)


    def test_get_mixed_sex_rooms_success(self):
        output=[("Room A",),("Room B",)]

        self.db_mock.execute_analysis_query.return_value= (True, output, 2)

        result = self.service.get_mixed_sex_rooms()
        
        self.assertEqual(result, output)
        self.db_mock.execute_analysis_query.assert_called_once()

    def test_get_mixed_sex_rooms_failed(self):
        self.db_mock.execute_analysis_query.return_value= (False, None, 0)
        result = self.service.get_mixed_sex_rooms()
        self.assertIsNone(result)




    def test_execute_all_analysis(self):
        #side effect here return one value by one !!!!
        self.db_mock.execute_analysis_query.side_effect =[
            (True, [("Room A", 5)], 1),
            (True, [("Room B", 20)], 1),
            (True, [("Room C", 10)], 1),
            (True, [("Room D",)], 1)
        ]

        result = self.service.execute_all_analysis()
        self.assertIn("count_by_room", result)
        self.assertIn("smallest_age_avg", result)
        self.assertIn("largest_age_diff", result)
        self.assertIn("mixed_sex_rooms", result)

        self.assertEqual(len(result),4)







if __name__ == '__main__':
    unittest.main()