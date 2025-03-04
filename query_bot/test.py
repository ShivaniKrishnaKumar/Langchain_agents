from pymongo import MongoClient

client = MongoClient("mongodb+srv://shivani:1234@cluster0.55ooy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["maars_bot"] 
collection = db["patient_details"] 

# Define the update query
filter_condition = { "patient_id": 2 }
update_operation = { "$set": { "Appointment Date": "2025-03-01" } }

# Execute the update operation
result = collection.update_one(filter_condition, update_operation)

# Check if the update was successful
if result.modified_count > 0:
    print("Document updated successfully")
else:
    print("No matching document found")
