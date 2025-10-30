import unittest
from unittest.mock import patch, MagicMock
from data_access import DBManager, DynamicLoader


class TestDBManager(unittest.TestCase):

    def setUp(self):
        self.db_params = {
              "dbname":"database", "user":"root", "password":"password", "host": "localhost","port":"5432"}
        
        self.db = DBManager(self.db_params)


    @patch("data_access.psycopg2.connect")
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


    @patch("data_access.psycopg2.connect")
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




if __name__ == '__main__':
    unittest.main()