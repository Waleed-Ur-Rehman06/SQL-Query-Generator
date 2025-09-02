import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, db_schema):
    """
    Generates an SQL query from a natural language question using the Gemini model.
    The prompt is dynamic and includes the current database schema.
    """
    # Dynamic prompt with schema information
    prompt = f"""
    You are an expert in converting English questions to SQLite SQL queries!
    The database schema is as follows:
    {db_schema}
    
    You need to write a SQL query to answer the user's question.
    
    **Important Rules:**
    1. The SQL query must be for a SQLite database.
    2. Only generate SELECT statements. Do not generate any INSERT, UPDATE, or DELETE queries.
    3. The SQL code should not have ``` in the beginning or end.
    4. Do not include the word 'sql' in the output.
    5. Be careful with column names, and use the exact column names from the schema.
    
    For example:
    Question: How many records are in the student table?
    SQL Command: SELECT COUNT(*) FROM STUDENT;
    
    Question: Show me the names of students in the 'Data Science' class.
    SQL Command: SELECT NAME FROM STUDENT WHERE CLASS = 'Data Science';
    
    Question: Tell me the names and marks of students who scored more than 90.
    SQL Command: SELECT NAME, MARKS FROM STUDENT WHERE MARKS > 90;
    
    Now, here is the user's question:
    """

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([prompt, question])
    return response.text