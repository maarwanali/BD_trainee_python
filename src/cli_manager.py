import argparse
import sys
from data_access import DynamicLoader, DBManager
from query_service import QueryService
from reporter import FormatterFactory
from writer import WriteToFile
import logging

logger = logging.getLogger(__name__)

class CLIManager:

    def __init__(self, db_params:dict):
        logger.info('CLI Manager initialized..')
        self.db_params = db_params
        self.db_manager = DBManager(self.db_params)
        self.data_loader = DynamicLoader(self.db_manager)
        self.query_service = QueryService(self.db_manager)
        self.factory = FormatterFactory()
        self.writer = WriteToFile()


    def _parse_arguments(self):
        parser = argparse.ArgumentParser(
            description="Process students and rooms data, run queries and generate reports",
            formatter_class=argparse.RawTextHelpFormatter

        )

        parser.add_argument('--students', required=True, help='path to students Json file.')
        parser.add_argument('--rooms', required=True, help='path to rooms Json file.')

        parser.add_argument('--format', required=True, choices=['json', 'xml'], help='Output format type: "json" | "xml"')

        return parser.parse_args()

    def run(self):

        try:
            args = self._parse_arguments()
            logger.info(" Starting Data Analysis Pipeline ")

            #load files to db 'data_access.py' DynamicLoader Class.
            self.data_loader.load_file(args.rooms, table_name='rooms')
            self.data_loader.load_file(args.students, table_name='students')
            
            #Running Optimization Inx

            self.db_manager.add_optimization_indexes()
            
            logger.info("Running Analytics Queries ")
            # Running all 4 queries
            raw_results = self.query_service.execute_all_analysis()

            # Check for critical errors during query execution
            if any(result is None for result in raw_results.values()):
                logger.error("One or more analytical queries failed during execution.")
                raise RuntimeError("One or more analytical queries failed during execution.")

            logger.info(f" Generating Report ({args.format.upper()})")
            

            formatter = self.factory.get_formatter(args.format)
            final_report_string = formatter.format(raw_results)

            if final_report_string is not None:
                self.writer.write(final_report_string, args.format)
            
            sys.exit(0) 

        except Exception as e:
            logger.error(f"\nERROR: Pipeline failed. Details: {e}")
            sys.exit(1) # Failure exit code        