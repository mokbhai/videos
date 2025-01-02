import json

def convert_json_to_text(json_file_path, output_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    with open(output_file_path, 'w') as output_file:
        for entry in data:
            output_file.write(entry['text'] + '\n')

if __name__ == "__main__":
    json_file_path = 'Developer/data.json'
    output_file_path = 'Text/output.txt'
    convert_json_to_text(json_file_path, output_file_path)
