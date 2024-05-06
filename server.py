from flask import Flask, make_response, request

# Create Flask app instance
app = Flask(__name__)

# Sample data
data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    ...
]

# Sends back implicit 200 OK response code
@app.route("/")
def index():
    return "hello world"

# Send custom HTTP response code back using tuple
@app.route("/nocontent")
def no_content():
    return ("hello world", 204)

# Send custom HTTP response and code back with the make_response() method
@app.route("/makeres")
def makeres():
    response = make_response({"message": "Hello World"})
    response.status_code = 202
    return response

# Route to get data
@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404

# Route for name search
@app.route("/name_search")
def name_search():
    """Find a person in the database."""
    query = request.args.get("q")

    if query == "":
        return {"message": "Invalid input parameter"}, 422

    for person in data:
        if query.lower() in person["first_name"].lower():
            return person

    return ({"message": "Person not found"}, 404)

# Route to count data
@app.get("/count")
def count():
    try:
        count = len(data)
        return ({"data count": count}, 200)
    except NameError:
        return ({"message": "No data list found"}, 500)

# Route to find person by UUID
@app.route("/person/<unique_id>")
def find_by_uuid(unique_id):
    for person in data:
        if person["id"] == str(unique_id):
            return person
    return {"message": "Unable to find person with uuid {unique_id}"}, 404

# Route to delete person by UUID
@app.route("/person/<uuid>", methods=["DELETE"])
def delete_uuid(uuid):
    # Check if the person with the specified UUID exists in the data list
    for person in data:
        if person["id"] == uuid:  # Comparing UUID strings directly
            data.remove(person)
            return {"message": f"Person with ID: {uuid} deleted"}, 200

    # If person not found, return 404 response
    return {"message": "Person not found in data list"}, 404

# Route to add new person
@app.route("/person", methods=["POST"])
def add_by_uuid():
    new_person = request.json
    if not new_person:
        return {"message": "Invalid input"}, 422
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500
    return {"message": f"{new_person['id']} was successfully created"}, 200

# Error handler for 404 Not Found
@app.errorhandler(404)
def api_not_found(error):
    return{"message": "API not found."}, 404