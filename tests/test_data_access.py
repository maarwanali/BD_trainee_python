import unittest
from unittest.mock import patch, MagicMock, mock_open
from src.data_access import DBManager, DynamicLoader

class TestDBManager(unittest.TestCase):

    def setUp(self):
        self.db_params = {
              "dbname":"database", "user":"root", "password":"password", "host": "localhost","port":"5432"}
        
        self.db = DBManager(self.db_params)


    @patch("src.data_access.psycopg2.connect")
    def test_execute_insert(self, mock_connect):
        # setup Mock

        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.rowcount=2

        query = "INSERT INTO students (name) VALUES (%s);"
        data = [("alice", "samar")]

        success, result,rowcount = self.db.execute_insert(query, data)

        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(rowcount,2)

        mock_cur.executemany.assert_called_once_with(query, data)
        mock_conn.commit.assert_called_once()


    @patch("src.data_access.psycopg2.connect")
    def test_execute_analysis_query(self, mock_connect):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.fetchall.return_value=[("alice",),( "samar",)]
        mock_cur.rowcount=2

        query='''' SELECT * FROM students '''

        success, result, rowcount = self.db.execute_analysis_query(query)

        self.assertTrue(success)
        self.assertIsNotNone(result)
        self.assertEqual(rowcount, 2)

        mock_cur.execute.assert_called_once_with(query)
        mock_cur.fetchall.assert_called_once()



class TestDynamicLoader(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock(DBManager)
        self.dy_loader = DynamicLoader(self.mock_db)

    @patch('src.data_access.json.load')
    @patch('src.data_access.open', new_callable=mock_open )
    def test_read_json(self,mock_open_fn, mock_json_load):
        mock_json_load.return_value = [{"id": 1, "name": "Room A"}]
        result = self.dy_loader._read_json_file("rooms.json")

        mock_open_fn.assert_called_once_with("rooms.json", 'r')
        mock_json_load.assert_called_once()

        self.assertEqual(result, [{"id": 1, "name": "Room A"}])



    def test_load_records(self):
        data = [{"id": 1, "name": "Room A"}, {"id": 2, "name": "Room B"}]
        self.dy_loader.db_manager.execute_insert.return_value = (True, None, 2)
        result = self.dy_loader._load_records(data, 'rooms')

        self.assertTrue(result[0])
        self.dy_loader.db_manager.execute_insert.assert_called_once()


    @patch.object(DynamicLoader, '_read_json_file')
    @patch.object(DynamicLoader, '_load_records')
    def test_load_file(self, mock_load_records, mock_read_json):
        mock_read_json.return_value = [{"id": 1, "name": "Room A"}]
        mock_load_records.return_value = (True, None, 1)

        self.dy_loader.load_file('rooms.json', 'rooms')

        mock_read_json.assert_called_once_with("rooms.json")
        mock_load_records.assert_called_once_with([{"id": 1, "name": "Room A"}], 'rooms')

if __name__ == '__main__':
    unittest.main()