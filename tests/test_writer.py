import unittest
from unittest.mock import patch, mock_open
from src.writer import WriteToFile


class TestWriteToFile(unittest.TestCase):
    def setUp(self):
        self.writer = WriteToFile()
        self.sample_data = '{"report":"test"}'
        self.format= "json"

    @patch("writer.os.path.isdir")
    @patch("writer.os.mkdir")
    @patch("writer.open", new_callable= mock_open)
    @patch("writer.datetime")
    def test_write_creates_file_folder(self, mock_datetime, mock_open_fn, mock_mkdir, mock_isdir):
        mock_isdir.return_value = False
        mock_datetime.now.return_value.strftime.return_value="2025-10-30-09-09-00"
        
        self.writer.write(self.sample_data, self.format)
        mock_mkdir.assert_called_once_with("output")

        mock_open_fn.assert_called_once_with("output/report2025-10-30-09-09-00.json","w")

        mock_open_fn().write.assert_called_once_with(self.sample_data)


    @patch("writer.open", new_callable=mock_open)
    @patch("writer.os.path.isdir", return_value=True)
    def test_write_handles_exceptions(self,mock_isdir, mock_open_fn):
        
        mock_open_fn.side_effect = IOError("No Space")

        with self.assertRaises(IOError):
            self.writer.write(self.sample_data, self.format)









if __name__ == '__main__':
    unittest.main()