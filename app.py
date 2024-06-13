from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import subprocess

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Example route to post data
@app.route('/api/data', methods=['POST'])
def post_data():
    
    input_data = request.json
    
    inkml = input_data.get('inkML')
    canvas_size = input_data.get('canvasSize')

    response_data = {
        'received': input_data
    }
    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'inkml_requests/{time_stamp}.inkml', 'w') as f:
        f.write(str(inkml))
    print('inkml', inkml)
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
    return jsonify(response_data)
  

if __name__ == '__main__':
    app.run(debug=True)
