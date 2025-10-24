import json
import psycopg2 
from psycopg2 import sql


class DBManager:
    ''' Handle DB connection, transactions, queries'''
    def __init__(self, db_params:dict ):
        self.db_params = db_params
        print("DB Manager initialized ...")


    def _execute_transaction(self, query:str, data:list =None, fetch:bool = False):

        conn = None
        result = None

        try:

            conn = psycopg2.connect(** self.db_params)
            cur = conn.cursor()

            if data:
                cur.executemany(query,data)

            else:
                cur.execute(query)

            if fetch:
                result = cur.fetchall()
            else:
                # Only commit if we modified data (no SELECT happened)
                conn.commit()

            cur.close()
            return result


        except (Exception, psycopg2.Error) as e:
            print(f"Error executing Sql Query: {e}")
            if conn :
                conn.rollback()

            return None

        finally:
            if conn is not None:
                conn.close()



    def execute_analysis_query(self, query:str):
        return self._execute_transaction(query, fetch=True)

    def execute_insert(self, query:sql.SQL, data:list):
        if not data:
            return
    
        success = self._execute_transaction(query = query, data= data)
        if not success:
            return None
        return True




class DynamicLoader:
    ''' Handle I/O, data transformation and loading into database'''

    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager
        print("dynamic loader initialized..")


    def _read_json_file(self, filepath:str)->list:
        with open(filepath ,'r') as f:
            return json.load(f)
       


    def _load_records(self, data_records:list, table_name:str):
        
        if not data_records:
            return
        cols = list(data_records[0].keys())

        sql_cols = sql.SQL(", ").join(map(sql.Identifier, cols))
        placeholders = sql.SQL(", ").join(sql.Placeholder() * len(cols)) # getting s%

        insert_query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values}) ON CONFLICT DO NOTHING;").format(
            table = sql.Identifier(table_name),
            columns = sql_cols,
            values= placeholders
        )

        records_to_insert = [tuple(record[col] for col in cols )for record in data_records]

        ### LOADING DATA TO DATABASE (DBManager)
        self.db_manager.execute_insert(insert_query, records_to_insert)


    def load_file(self, filepath:str, table_name:str):
        try:
            records = self._read_json_file(filepath)
            self._load_records(records, table_name)
            print(f"Data Successfully loaded to {table_name} & number of records:{len(records)}. ")
        except Exception as e :
            print(f"postgres error: {e}")
