import argparse
import sys
from data_access import DynamicLoader, DBManager
from services import QueryService
from reporter import ReportFormatter



class CLIManager:

    def __init__(self, db_params:dict):
        self.db_params = db_params

        self.db_manager = DBManager(self.db_params)
        self.data_loader = DynamicLoader(self.db_manager)
        self.query_service = QueryService(self.db_manager)

        self.report_formatter = ReportFormatter()


        print("CLI initialized ...")

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
            print("--- Starting Data Analysis Pipeline ---")

            #load files to db 'data_access.py' DynamicLoader Class.
            self.data_loader.load_file(args.rooms, table_name='rooms')
            self.data_loader.load_file(args.students, table_name='students')
            
            print("\n--- Running Analytics Queries ---")
            # Running all 4 queries
            raw_results = self.query_service.execute_all_analysis()

            # Check for critical errors during query execution
            if any(result is None for result in raw_results.values()):
                raise RuntimeError("One or more analytical queries failed during execution.")

            print(f"\n--- Generating Report ({args.format.upper()}) ---")
            
            # Format the data using the  ReportFormatter i reporter.py
            final_report_string = self.report_formatter.format_output(
                raw_results, 
                args.format
            )

            # --- Final Output ---
            print("\n" + "="*50)
            print(final_report_string)
            print("="*50)
            
            sys.exit(0) 

        except Exception as e:
            print(f"\nERROR: Pipeline failed. Details: {e}", file=sys.stderr)
            sys.exit(1) # Failure exit code        