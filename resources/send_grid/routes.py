from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')

@app.route('/submitintake', methods=['POST'])
def submit_intake():
    form_data = request.json  

    try:
        send_email(form_data)
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_email(form_data):
    message = Mail(
        from_email='buhaymalaya@icloud.com',  
        to_emails='buhaymalaya@icloud.com',  
        subject='Intake Form Submission',
        html_content='Intake Form Submission:<br>' +
                     f'First Name: {form_data.get("firstName")}<br>' +
                     f'Last Name: {form_data.get("lastName")}<br>' +
                     '--- End of Form ---'
    )

    sg = SendGridAPIClient(sendgrid_api_key)

    response = sg.send(message)
    return response
    

if __name__ == '__main__':
    app.run(debug=True)
