from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import subprocess
import os
import time
import ast

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Example route to post data
@app.route('/api/data', methods=['POST'])
def post_data():
    
    input_data = request.json
    
    inkml = input_data.get('inkML')
    canvas_size = input_data.get('canvasSize')

    # response_data = {
    #     'received': input_data
    # }
    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'inkml_requests/{time_stamp}.inkml', 'w') as f:
        f.write(str(inkml))
    # Command to execute the script
    command = [
        'python', 'main.py',
        '--inkml', f'inkml_requests/{time_stamp}.inkml',
        '--other_ratio', f'{canvas_size}',
        '--production', 'True'
    ]
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)   
    
    # Capture the output and error
    output = result.stdout
    error = result.stderr 
    
    # Log the output and error
    app.logger.info(output)
    app.logger.error(error) 
    
    # Wait for the result file to be created
    while not os.path.exists(f'inkml_results/{time_stamp}.txt'):
        time.sleep(0.1)  # Sleep briefly to avoid busy-waiting
        
    data = None
    with open(f'inkml_results/{time_stamp}.txt', 'r') as f:
        data = f.read()
    
    response_data = []
    for data in ast.literal_eval(data):
        if 'valid' in data:
            response_data.append(data['valid'])
    # remove file from inkml_requests and inkml_results
    os.remove(f'inkml_requests/{time_stamp}.inkml')
    os.remove(f'inkml_results/{time_stamp}.txt')
    
    return jsonify({'received': input_data, 'result': response_data})
  

if __name__ == '__main__':
    app.run(debug=True)
