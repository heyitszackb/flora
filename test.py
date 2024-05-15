import json

def test_file_writing():
    data = {"test": "This is a test"}
    try:
        with open("test_export.json", 'w') as file:
            json.dump(data, file)
            print("Test file written successfully.")
    except Exception as e:
        print("Error writing test file:", e)

test_file_writing()