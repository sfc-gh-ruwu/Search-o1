import json

# Load JSON data from a file
with open("/Users/ruwu/Research/Dataset/bamboogle_125.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Initialize an empty list to store the filtered results
filtered_data = []

# Iterate through each item and create a new dictionary with selected keys
for item in data:
    new_item = {
        "id": item.get("id"),
        "Question": item.get("question"),
        "answer": item.get("golden_answers")
    }
    filtered_data.append(new_item)  # Append the new dictionary to the list

# Save the filtered results to a new JSON file
with open("./QA_Datasets/bamboogle.json", "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, indent=4)
