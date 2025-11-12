import unittest
from src.reporter import FormatterFactory, JsonFormatter, XmlFormatter
import json
import xml.etree.ElementTree as ET

class TestFormatterFactory(unittest.TestCase):

    def setUp(self):
        self.factory = FormatterFactory()
        


    def test_get_xml_formatter(self):

        format = self.factory.get_formatter('xml')
        self.assertIsInstance(format, XmlFormatter)


    def test_get_json_formatter(self):
        format = self.factory.get_formatter('json')
        self.assertIsInstance(format, JsonFormatter)


    def test_get_invalid_formatter(self):
        with self.assertRaises(ValueError):
            self.factory.get_formatter('txt')



class TestJsonFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = JsonFormatter()

    def test_format_count_by_room(self):
        input_data = {
            "count_by_room": [("Room A", 5), ("Room B", 3)]
        }

        result = self.formatter.format(input_data)
        parsed = json.loads(result)
        self.assertIn("report_metadata", parsed)
        self.assertIn("analysis_results", parsed)
        self.assertEqual(len(parsed["analysis_results"]["count_by_room"]), 2)
        self.assertEqual(parsed["analysis_results"]["count_by_room"][0]["room_name"],"Room A" )

    
    def test_format_smallest_age_avg(self):
        input_data = {
            "smallest_age_avg":[("Room A", 15), ("Room B", 20)]
        }

        result = self.formatter.format(input_data)
        parsed = json.loads(result)

        self.assertEqual(len(parsed["analysis_results"]["smallest_age_avg"]), 2)
        self.assertEqual(parsed["analysis_results"]["smallest_age_avg"][0]["age_avg"], 15)
    
    def test_format_largest_age_diff(self):
        input_data = {
        "largest_age_diff":[("Room A", 15), ("Room B", 20)]
        }

        result = self.formatter.format(input_data)
        parsed = json.loads(result)

        self.assertEqual(len(parsed["analysis_results"]["largest_age_diff"]), 2)
        self.assertEqual(parsed["analysis_results"]["largest_age_diff"][0]["age_diff"], 15)

    def test_format_mixed_sex_rooms(self):
        input_data ={
            "mixed_sex_rooms": [("Room A",), ("Room B",)]
        }

        result = self.formatter.format(input_data)
        parsed = json.loads(result)

        self.assertEqual(len(parsed["analysis_results"]["mixed_sex_rooms"]), 2)
        self.assertEqual(parsed["analysis_results"]["mixed_sex_rooms"][0]["room_name"], "Room A")

    def test_format_with_none_data(self):
        input_data = {
            "count_by_room": None
        }
        result = self.formatter.format(input_data)
        parsed = json.loads(result)
        self.assertEqual(parsed["analysis_results"]["count_by_room"], "QUERY FAILED")

class TestXmlFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = XmlFormatter()


    def test_count_by_room(self):
        input_data = {
            "count_by_room": [("Room A", 5), ("Room B", 3)]
        }

        result = self.formatter.format(input_data)
        root = ET.fromstring(result)

        self.assertEqual(root.tag, "Report")

        count_by_room  = root.find("countbyroom")
        self.assertIsNotNone(count_by_room)
        rooms = count_by_room.findall("RoomEntry")
        self.assertEqual(len(rooms),2)
        self.assertEqual(rooms[0].find("RoomName").text, "Room A")

    def test_smallest_age_avg(self):
        input_data = {
            "smallest_age_avg":[("Room A", 15), ("Room B", 20)]
        }   
        
        result = self.formatter.format(input_data)
        root = ET.fromstring(result)

        smallest_age_avg = root.find("smallestageavg")
        self.assertIsNotNone(smallest_age_avg)
        rooms = smallest_age_avg.findall("RoomEntry")
        self.assertEqual(len(rooms),2)
        self.assertEqual(int(rooms[0].find("AvgValue").text), 15)


    def test_largest_age_diff(self):
        input_data = {
            "largest_age_diff":[("Room A", 15), ("Room B", 20)]
        }   
        
        result = self.formatter.format(input_data)
        root = ET.fromstring(result)

        smallest_age_avg = root.find("largestagediff")
        self.assertIsNotNone(smallest_age_avg)
        rooms = smallest_age_avg.findall("RoomEntry")
        self.assertEqual(len(rooms),2)
        self.assertEqual(int(rooms[0].find("DiffValue").text), 15)

    def test_format_mixed_sex_rooms(self):
        input_data ={
            "mixed_sex_rooms": [("Room A",), ("Room B",)]
        }
        result = self.formatter.format(input_data)
        root = ET.fromstring(result)

        mixed_sex_rooms = root.find("mixedsexrooms")
        self.assertIsNotNone(mixed_sex_rooms)
        rooms = mixed_sex_rooms.findall("RoomName")
        self.assertEqual(len(rooms), 2)
        self.assertEqual(rooms[0].text, 'Room A')

    def test_format_with_none_data(self):
        input_data = {
            "count_by_room": None
        }
        result = self.formatter.format(input_data)
        root = ET.fromstring(result)
        count_by_room = root.find("countbyroom")
        self.assertIsNone(count_by_room)

if __name__ == '__main__':
    unittest.main()