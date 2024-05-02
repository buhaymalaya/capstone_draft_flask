from flask import Flask, request, jsonify
import os
import base64
from flask_cors import CORS
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileName,FileType, FileContent, Disposition

# load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# retrieve the SendGrid API key from the environment variable
sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')

@app.route('/submitintake', methods=['POST'])
# def submit_intake():
#     form_data = request.json  

#     try:
#         send_email(form_data)
#         return jsonify({'message': 'Email sent successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

def send_email(form_data):
    form_data = request.json  
    
    to_email = form_data['to'],  
    subject = form_data['subject'], 
    content = form_data['text'],
    pdf_data = form_data['pdf_data'] # double check if pdf is base64 encoded string

    pdf_bytes = base64.b64decode(pdf_data)

    message = Mail(
        from_email = 'buhaymalaya@icloud.com',
        to_emails = 'buhaymalaya@icloud.com',
        subject = '',
        content = ''
    )
    
    attachment = Attachment (
        FileContent(base64.b64encode(pdf_bytes).decode()),
        FileName('attachment.pdf'),
        FileType('application/pdf'),
        Disposition('attachment')
    )

    message.attachment = attachment

    sg = SendGridAPIClient(sendgrid_api_key)

    try:
        response = sg.send(message)
        return {'message': 'Email sent successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True)  
