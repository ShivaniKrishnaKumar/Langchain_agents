from langchain.agents import Tool
from langchain.tools.base import StructuredTool
from pymongo import MongoClient
from langchain_experimental.utilities import PythonREPL

client = MongoClient("mongodb+srv://shivani:1234@cluster0.55ooy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["maars_bot"] 
collection = db["patient_details"] 

def fetch_document(query: dict):
    """
    Fetches the relevant appointment records based on a query. The query should include at least one of the following fields:
        - patient_id: integer (the patient's unique ID, if specified)
        - Name: string (the name of the patient, if specified)
        - Appointment Date: string (the date of the appointment in YYYY-MM-DD format, if specified)
        - Time Slot: string (the time of the appointment in HH:MM AM/PM format, if specified)
    
    Ensure all date values are output as properly formatted ISO 8601 strings (YYYY-MM-DD). Do not use Python code
    For example:
    To fetch a document using the patient ID 1234, the following query is used:
    {'patient_id': 1234}
    NOTE: All the value should be in lowercase.
    """
    client = MongoClient("mongodb+srv://shivani:1234@cluster0.55ooy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["maars_bot"]
    collection = db["patient_details"]
    print(f"connected with {collection} succesfully.....")
    # # Convert query keys to match the database schema
    schema_query = {}
    for key, value in query.items():
        if key == "patient_id":
            schema_query["patient_id"] = int(value)  # Ensure patient_id is an integer

    print("Processed Query:", schema_query)  # Debugging: Print the processed query

    # Fetch documents from the collection
    print(query)
    docs = [doc for doc in collection.find(schema_query)]
    print("Query Results:", docs)  # Debugging: Print the query results

    return str(docs)

def delete_document(filter: dict):
    """ Removes the relevant appointment records based on a delete query. The query should include:
        - A filter to identify which document(s) to delete (e.g., by _id, Name, Appointment Date, or other criteria).

    Ensure all date values are output as properly formatted ISO 8601 strings (YYYY-MM-DD). Do not use Python code
    For example:
    To delete a document using the patient ID 1234, the following filter is used:
    {"patient_id": 1234}

    NOTE: All values should be in lowercase.
    """
    client = MongoClient("mongodb+srv://shivani:1234@cluster0.55ooy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["maars_bot"] 
    collection = db["patient_details"] 
    print(filter)
    collection.delete_one(dict(filter))
    return "Document deletion successful."


def update_document(filter: dict, update: dict):
    """
    Modifies the relevant appointment records based on a query. The query should include:
        - A filter to identify which document(s) to update (e.g., by _id, Name, Appointment Date, or other criteria).
        - The fields to be updated along with their new values.
        - Ensure that `Appointment Date` is always in `ISODate` format (YYYY-MM-DD).
    For example:
    To update the time slot for a specific appointment, the following query is used:
    {
        "filter": { "patient_id": 1234},
        "update": { "$set": { "Time Slot": "11:00 AM" } }
    }
    to update the appointment date for a specific appointment, the following query is used:
    {
    "filter": { "patient_id": 1234 },
    "update": { "$set": { "Appointment Date": new Date("2025-03-05") } }
    }

    NOTE: All values should be in lowercase.
    """
    client = MongoClient("mongodb+srv://shivani:1234@cluster0.55ooy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["maars_bot"] 
    collection = db["patient_details"] 
    collection.update_one(dict(filter), dict(update))
    return "Document updation successful."


fetch_tool = StructuredTool.from_function(
    func=fetch_document
)

update_tool = StructuredTool.from_function(
    func=update_document
)

delete_tool = StructuredTool.from_function(
    func=delete_document
)
python_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=PythonREPL().run,
)