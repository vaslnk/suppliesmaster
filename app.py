import re

from flask import Flask, render_template_string
import gspread
import json
import os
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Google Sheets setup .
SCOPE = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = 'suppliersmaster-697acdbd6c87.json'

credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPE)
# Convert the string from the environment variable back into a dictionary
#service_account_info = json.loads(os.environ.get('GOOGLE_CREDENTIALS').replace('\\n', '\n'))
#credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPE)

gc = gspread.authorize(credentials)

# Open the spreadsheet by ID
spreadsheet_id = '19vp-zb0XbdlpGozwSSjI6bpn_XNki_yiDQYNlqUVEK4'
worksheet = gc.open_by_key(spreadsheet_id).get_worksheet(2)


def make_urls_clickable(text):
    # Regular expression to find URLs in text
    url_pattern = re.compile(r'https?://\S+')

    # Replace URLs with clickable links
    return url_pattern.sub(lambda x: f'<a href="{x.group()}">{x.group()}</a>', text)


@app.route('/')
def home():
    # Fetch all the records
    records = worksheet.get_all_records()

    # Convert URLs in records to clickable links
    for row in records:
        for key, value in row.items():
            if isinstance(value, str) and 'http' in value:
                row[key] = make_urls_clickable(value)
    
    # Enhanced HTML with Bootstrap for styling
    table_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Suppliers Data</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { padding: 20px; }
                .table-container { margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container-fluid">
                <h2 class="my-4">Suppliers Data</h2>
                <div class="table-container">
                    <table class="table table-bordered table-hover" id="dataTable">
                        <thead class="thead-dark">
                            <tr>
                                {% for header in records[0].keys() %}
                                <th scope="col">
                                    {{ header }}
                                    <input type="text" class="form-control filter-input" data-column="{{ loop.index0 }}" placeholder="Filter">
                                </th>
                                {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in records %}
                            <tr>
                                {% for cell in row.values() %}
                                <td>{{ cell | safe }}</td>
                                {% endfor %}
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            <!-- Bootstrap JS and dependencies -->
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
            <script>
                $(document).ready(function() {
                    $('.filter-input').on('keyup', function() {
                        var columnIndex = $(this).data('column');
                        var filterValue = $(this).val().toUpperCase();
                        $('#dataTable tbody tr').each(function() {
                            var cellText = $(this).find('td').eq(columnIndex).text().toUpperCase();
                            if (cellText.indexOf(filterValue) > -1) {
                                $(this).show();
                            } else {
                                $(this).hide();
                            }
                        });
                    });
                });
            </script>
        </body>
        </html>
        """

    return render_template_string(table_html, records=records)

if __name__ == '__main__':
    app.run(debug=True)
