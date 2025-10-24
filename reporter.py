import json 
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod



class ReportFormatter:
    
    def __init__(self):
        print("ReportFormatter initialized..")

    def format_output(self, raw_results : dict, output_format:str):
        formatters = {

            'json': self._format_json,
            'xml': self._format_xml

        }

        if output_format not in formatters:
            return f"Error currently {output_format} Unsupported."

        report_result = formatters[output_format](raw_results) # calling function from formatter dict

        return report_result


    def _format_json(self, raw_results:dict):
        pass

    def _format_xml(self, raw_results:dict):
        pass      