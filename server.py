from flask import Flask, make_response, request
app = Flask(__name__)

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
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]


# Sends back implicit 200 OK response code
@app.route("/")
def index():
    return "hello world"

# Send custom HTTP response code back using tuple
@app.route("/nocontent")
def no_content():
    return ("hello world", 204)

#Send custom HTTP response and code back with the make_response() method.
@app.route("/makeres")
def makeres():
    response = make_response({"message": "Hello World"})
    response.status_code = 202
    return response

@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404

@app.route("/name_search")
def name_search():
    """find a person in the database
        Returns:
        json: person if found, with status of 200
        404: if not found
        422: if argument q is missing
    """
    query = request.args.get("q")

    if query == "":
        return {"message": "Invalid input parameter"}, 422

    for person in data:
        if query.lower() in person["first_name"].lower():
            return person

    return ({"message": "Person not found"}, 404)

@app.get("/count")
def count():
    try:
        count = len(data)
        return ({"data count": count}, 200)
    except NameError:
        return ({"message": "No data list found"}, 500)

@app.route("/person/<unique_id>")
def find_by_uuid(unique_id):
    for person in data:
        if person["id"] == str(unique_id):
            return person
    return {"message": "Unable to find person with uuid {unique_id}"}, 404

@app.route("/person/<uuid>", methods=["DELETE"])
def delete_uuid(uuid):
    # Check if the person with the specified UUID exists in the data list
    for person in data:
        if person["id"] == uuid:  # Comparing UUID strings directly
            data.remove(person)
            return {"message": f"Person with ID: {uuid} deleted"}, 200

    # If person not found, return 404 response
    return {"message": "Person not found in data list"}, 404

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

@app.errorhandler(404)
def api_not_found(error):
    return{"message": "API not found."}, 404
