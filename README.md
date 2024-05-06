# Flask Practice Lab

This Flask application provides various routes for practicing handling HTTP requests and responses.

## Routes:
/ - Returns "hello world".
/nocontent - Returns "hello world" with a 204 No Content status code.
/makeres - Returns a custom HTTP response with status code 202.
/data - Returns information about the sample data.
/name_search?q=<query> - Searches for a person in the sample data by first name.
/count - Returns the count of items in the sample data.
/person/<unique_id> - Finds a person in the sample data by UUID.
/person/<uuid> (DELETE) - Deletes a person from the sample data by UUID.
/person (POST) - Adds a new person to the sample data.

Error Handling
404 Not Found: If an API endpoint is not found.