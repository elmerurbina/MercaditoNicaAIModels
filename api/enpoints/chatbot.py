import requests
from fastapi import APIRouter, HTTPException
import csv

router = APIRouter()

# URL for the external API where the question is fetched
EXTERNAL_API_URL = "http://external-api-url.com/get-question"

# Path to the CSV file
CSV_FILE_PATH = r"C:\Users\elmer\PycharmProjects\MercaditoNicaAIModels\api\endpoints\asistente.csv"

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

@router.post("/chatbot/")
async def get_response():
    """
    Get a question from an external API, then search for an answer in the local CSV file.
    """
    try:
        # Step 1: Fetch the question from the external API
        response = requests.get(EXTERNAL_API_URL)  # Assuming a GET request to fetch the question

        if response.status_code == 200:
            data = response.json()
            question = data.get("question")

            if question:
                # Step 2: Search for the answer in the local CSV dataset
                question_lower = question.lower()
                if question_lower in chatbot_data:
                    return {"answer": chatbot_data[question_lower]}
                else:
                    return {"answer": "Lo siento, no encuentro una respuesta a esta pregunta."}
            else:
                return {"answer": "Lo siento, no se pudo obtener la pregunta de la API externa."}
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching question from external API")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error communicating with external API")
