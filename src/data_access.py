import json
import psycopg2 
from psycopg2 import sql
import logging

logger = logging.getLogger(__name__)



class DBManager:
    ''' Handle DB connection, transactions, queries'''
    def __init__(self, db_params:dict ):
        self.db_params = db_params
        logger.info("DB Manager initialized ...")


    def _execute_transaction(self, query:str, data:list =None, fetch:bool = False):

        conn = None
        result = None
        rowcount = 0
        
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

            rowcount = cur.rowcount
            cur.close()
            return True ,result, rowcount


        except (Exception, psycopg2.Error) as e:
            logger.error(f"Error executing Sql Query: {e}")
            if conn :
                conn.rollback()

            return False , None,0

        finally:
            if conn is not None:
                conn.close()


    def execute_insert(self, query:sql.SQL, data:list):
        if not data:
            return None
        return self._execute_transaction(query=query, data=data)

        
        # if not data:
        #     return
    
        # success, result = self._execute_transaction(query = query, data= data)
        # if not success or not result:
        #     return None
        # return True

    def execute_analysis_query(self, query:str):
        return self._execute_transaction(query, fetch=True)

    
    def add_optimization_indexes(self):

        INDEX_STUDENTS_ROOM = "CREATE INDEX IF NOT EXISTS idx_students_room_id ON students (room);"
        INDEX_ROOMS_NAME = "CREATE INDEX IF NOT EXISTS idx_rooms_name ON rooms (name);"
        logger.info("Optimizing tables with indexes...")
    
        self._execute_transaction(INDEX_STUDENTS_ROOM)        
        self._execute_transaction(INDEX_ROOMS_NAME) 
        
        logger.info("Indexing complete.")



class DynamicLoader:
    ''' Handle I/O, data transformation and loading into database'''

    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager
        logger.info("dynamic loader initialized..")


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
        return self.db_manager.execute_insert(insert_query, records_to_insert)


    def load_file(self, filepath:str, table_name:str):
        try:
            records = self._read_json_file(filepath)
            success, _ ,rowcount = self._load_records(records, table_name)
            if not success:
                logger.error("Error occurs while executing Query.")
            elif success and rowcount == 0:
                logger.info("Query Success but no affected raws.")
            elif success and rowcount >0:
                logger.info(f"Data Successfully loaded to {table_name} & number of records:{len(records)}. ")
        except Exception as e :
            logger.error(f"postgres error: {e}")
