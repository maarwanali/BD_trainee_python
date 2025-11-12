from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

class WriteToFile:
    
    def write(self, data, format):

        try: 
            if not os.path.isdir('output/'):
                logger.info('Creating output folder..')
                os.mkdir('output')

            with open(f"output/report{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.{format}", 'w') as f:
                f.write(data)

            logger.info('File written successfully to output/')

        except Exception as e :
            logger.error("Error rasing while writing to output")
            raise e

            