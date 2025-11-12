from data_access import DBManager
from abc import ABC, abstractmethod
import logging

# List of rooms and the number of students in each of them
# 5 rooms with the smallest average age of students
# 5 rooms with the largest difference in the age of students
# List of rooms where different-sex students live

logger = logging.getLogger(__name__)



class IQueryService(ABC):
    @abstractmethod
    def get_students_count_by_room(self):
        pass

    @abstractmethod
    def get_rooms_by_smallest_age_avg(self):
        pass

    @abstractmethod
    def get_rooms_by_largest_def_age(self):
        pass

    @abstractmethod
    def get_mixed_sex_rooms(self):
        pass

class QueryService(IQueryService):

    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager
        
    
    def _run_query(self, query):
        
        success,result, _ =  self.db_manager.execute_analysis_query(query)
        if not success:
                logger.error("Error occurs while executing Query.")
                return None
        return result
         

    def get_students_count_by_room(self):
        query = """ 
            SELECT r.name, COUNT(s.id) 
            FROM rooms r 
            JOIN students s ON r.id = s.room
            GROUP BY r.name;
        """
        return self._run_query(query)
        


    def get_rooms_by_smallest_age_avg(self):
        query = """ 
            SELECT r.name, AVG(DATE_PART('year', AGE(s.birthday))) AS avg_age
            FROM rooms r 
            JOIN students s ON r.id = s.room
            GROUP BY r.name
            ORDER BY avg_age ASC
            LIMIT 5;
        """
        return self._run_query(query)
    
    def get_rooms_by_largest_def_age(self):
        query=""" 
            SELECT r.name AS room_name,
            EXTRACT(YEAR FROM AGE(MAX(s.birthday), MIN(s.birthday))) AS age_difference_years
            FROM rooms r 
            JOIN students s ON r.id = s.room
            GROUP BY  r.name
            HAVING COUNT(s.id) > 1
            ORDER BY age_difference_years DESC 
            LIMIT 5;
        """
        return self._run_query(query)

    def get_mixed_sex_rooms(self):
        query = """ 
            SELECT r.name
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY r.name
            HAVING COUNT(DISTINCT s.sex) > 1;
        """
        return self._run_query(query)
        
            

    def execute_all_analysis(self):
        print("Executing all analytical queries...")
        return {
            'count_by_room': self.get_students_count_by_room(),
            'smallest_age_avg': self.get_rooms_by_smallest_age_avg(),
            'largest_age_diff': self.get_rooms_by_largest_def_age(),
            'mixed_sex_rooms': self.get_mixed_sex_rooms()
        }