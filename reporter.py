import json 
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class IFormatter(ABC):
    @abstractmethod
    def format(self, raws_data:dict):
        pass


class FormatterFactory:
    def __init__(self):
        self._formatters = {
            'json': JsonFormatter(),
            'xml': XmlFormatter()
        }

    def get_formatter(self, format:str):
        formatter = self._formatters.get(format.lower())
        if not formatter:
            logger.error("File type not valid")
            raise ValueError("Format type does not correct")
        
        return formatter

class JsonFormatter(IFormatter):

    def format(self, raws_data:dict):
        today = datetime.now()

        report_data = {

            "report_metadata":{
                "generation_time": today
            },
            "analysis_results":{}
        }

        for query_name, data_records in raws_data.items():
            if data_records is None:
                report_data["analysis_results"][query_name] ="QUERY FAILED"
                continue

            formatted_list = []

            if query_name == 'count_by_room':
                for room_name,count in data_records:
                    formatted_list.append({"room_name": room_name, "students_count":count})

        
            elif query_name in ("smallest_age_avg", "largest_age_diff"):
                for room_name, metric_value in data_records:
                    metric_key = query_name.split('_')[-1]
                    formatted_list.append({"room_name": room_name, f"age_{metric_key}": metric_value})

            elif query_name == "mixed_sex_rooms":
                for room_tuple, in data_records:
                    formatted_list.append({"room_name":room_tuple})


            report_data["analysis_results"][query_name] = formatted_list
        return json.dumps(report_data, indent=4,default=str)
        

class XmlFormatter(IFormatter):

    def format(self, raws_data:dict):
        root = ET.Element("Report")

        meta = ET.SubElement(root, 'MetaData')
        ET.SubElement(meta, 'Format').text='XML'

        for query_name, data_records in raws_data.items():
            
            if data_records is None: continue

            query_group = ET.SubElement(root, query_name.replace('_',''))

            if query_name =='count_by_room':
                for room_name, count in data_records:
                    room_elem = ET.SubElement(query_group, 'RoomEntry')
                    ET.SubElement(room_elem,'RoomName').text = room_name
                    ET.SubElement(room_elem, 'Count').text= str(count )

            elif query_name in ("smallest_age_avg", "largest_age_diff"):
                for room_name, metric_value in data_records:
                    room_elem= ET.SubElement(query_group, 'RoomEntry')
                    ET.SubElement(room_elem,"RoomName").text = room_name

                    metric_tag = query_name.split('_')[-1].capitalize() + 'Value'

                    ET.SubElement(room_elem, metric_tag).text = str(metric_value)
            elif query_name == 'mixed_sex_rooms':
                for room_tuple, in data_records:
                    room_elem = ET.SubElement(query_group, 'RoomName')
                    room_elem.text = room_tuple
        

        ET.indent(root)
        return ET.tostring(root,encoding='unicode')

