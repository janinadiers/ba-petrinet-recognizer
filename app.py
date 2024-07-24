from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import subprocess
import os
import time
import ast
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Example route to post data
@app.route('/api/data', methods=['POST'])
def post_data():
    
    input_data = request.json
    
    inkml = input_data.get('inkML')
    canvas_size = input_data.get('canvasSize')
    # print('inkml: ', inkml)
    # response_data = {
    #     'received': input_data
    # }
    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print('time_stamp: ', time_stamp)
    with open(f'inkml_requests/{time_stamp}.inkml', 'w') as f:
        f.write(str(inkml))
    print('after writing inkml file', f'inkml_requests/{time_stamp}.inkml')
    try:
        # Command to execute the script
        command = [
            'python', 'main.py',
            '--inkml', f'inkml_requests/{time_stamp}.inkml',
            '--other_ratio', f'{canvas_size}',
            '--production', 'True'
        ]
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True) 
        print(result.stdout)
        print(result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
    # Capture the output and error
    output = result.stdout
    error = result.stderr 
    
    # Log the output and error
    app.logger.info(output)
    app.logger.error(error) 
    
    # Wait for the result file to be created
    while not os.path.exists(f'inkml_results/{time_stamp}.json'):
        time.sleep(0.1)  # Sleep briefly to avoid busy-waiting
        
    data = None
    
    with open(f'inkml_results/{time_stamp}.json', 'r') as f:
        data = json.load(f)
        
        # print('data: ', data)
    response_data = []
    
    for item in data:
        response_data.append(item)
    # remove file from inkml_requests and inkml_results
    os.remove(f'inkml_requests/{time_stamp}.inkml')
    os.remove(f'inkml_results/{time_stamp}.json')
    
    # Create the response object
    response = jsonify({'received': input_data, 'result': response_data})
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response
  

if __name__ == '__main__':
    app.run(debug=True)
