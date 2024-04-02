from flask import Flask, render_template_string
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Google Sheets setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = 'suppliersmaster-697acdbd6c87.json'

#credentials = Credentials.from_service_account_file(
#        SERVICE_ACCOUNT_FILE, scopes=SCOPE)
# Convert the string from the environment variable back into a dictionary
service_account_info = json.loads(os.environ.get('GOOGLE_CREDENTIALS').replace('\\n', '\n'))
credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPE)

gc = gspread.authorize(credentials)

# Open the spreadsheet by ID
spreadsheet_id = '19vp-zb0XbdlpGozwSSjI6bpn_XNki_yiDQYNlqUVEK4'
worksheet = gc.open_by_key(spreadsheet_id).sheet1

@app.route('/')
def home():
    # Fetch all the records
    records = worksheet.get_all_records()
    
    # Basic HTML table format for displaying the records
    table_html = """
    <html>
        <head>
            <title>Google Sheets Data</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h2 { color: #333; }
                table { border-collapse: collapse; width: 100%; }
                th, td { text-align: left; padding: 8px; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                th { background-color: #4CAF50; color: white; }
            </style>
        </head>
        <body>
            <h2>Google Sheets Data</h2>
            <table>
                <tr>
                    {% for header in records[0].keys() %}
                    <th>{{ header }}</th>
                    {% endfor %}
                </tr>
                {% for row in records %}
                <tr>
                    {% for cell in row.values() %}
                    <td>{{ cell }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
        </body>
    </html>
    """
    
    return render_template_string(table_html, records=records)

if __name__ == '__main__':
    app.run(debug=True)
