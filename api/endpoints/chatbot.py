from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import csv

router = APIRouter()

# Path to the CSV file
CSV_FILE_PATH = 'api/endpoints/asistente.csv'

# Load the CSV data into a dictionary
def load_csv_data(filepath):
    dataset = {}
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                dataset[row['question'].lower()] = row['answer']
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="CSV file not found")
    return dataset

# Load the data from asistente.csv
chatbot_data = load_csv_data(CSV_FILE_PATH)

# Define the input model
class QuestionModel(BaseModel):
    question: str

@router.post("/chatbot/")
async def get_response(question: QuestionModel):
    """
    Search for an answer in the local CSV file based on the user's question.
    """
    question_lower = question.question.lower()
    if question_lower in chatbot_data:
        return {"answer": chatbot_data[question_lower]}
    else:
        return {"answer": "Lo siento, no encuentro una respuesta a esta pregunta."}
