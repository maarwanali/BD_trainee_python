from datetime import datetime

class WriteToFile:
    
    def write(self, data, format):

        with open(f"output/report{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.{format}", 'w') as f:
            f.write(data)