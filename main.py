from cli_manager import CLIManager

# python main.py --students ./data/students.json --rooms ./data/rooms.json --format json

if __name__ == '__main__' :

    DB_CONFIG ={
    "dbname":"database",
    "user":"root",
    "password":"password",
    "host": "localhost",
    "port":"5432"
    }      

    manager = CLIManager(DB_CONFIG)
    manager.run()