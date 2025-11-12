# Python SQL-Based Room Analytics

This project loads student and room data from files located in the `/data` directory into a PostgreSQL database. It performs analytical queries directly in SQL to extract insights. Results are exported in either JSON or XML format to the `/output` directory.

---

## How to Run

### 1. Environment Setup
- Create a `.env` file in the project root with your PostgreSQL credentials.
- Ensure Docker and Docker Compose are installed to run the database container.

### 2. Database Initialization
- Use Docker Compose to start the PostgreSQL service.
- Manually create the required tables (`rooms` and `students`) in the database.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run Scripts
``` bash
python main.py \
  --students ./data/students.json \   # Path to students file
  --rooms ./data/rooms.json \         # Path to rooms file
  --format json                       # Output format: json or xml
```