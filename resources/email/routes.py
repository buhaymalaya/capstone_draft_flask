from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'esc.advocate@gmail.com'
app.config['MAIL_PASSWORD'] = 'SMTP_PASSWORD'

# initialize Flask-Mail
mail = Mail(app)

@app.route('/send-pdf', methods=['POST'])
def send_pdf():
    try:
        pdf_data = request.json.get('pdfData')

        # Send email with Flask-Mail
        msg = Message(subject='PDF Attachment', recipients=['malayabuhay@gmail.com'], body='See attached PDF')
        msg.attach('document.pdf', 'application/pdf', pdf_data)
        mail.send(msg)

        return jsonify({'message': 'PDF sent successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
