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
worksheet = gc.open_by_key(spreadsheet_id).sheet1

@app.route('/')
def home():
    # Fetch all the records
    records = worksheet.get_all_records()
    
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
            <input type="text" id="filterInput" placeholder="Filter by keyword" class="form-control mb-3">
            <button onclick="filterTable()" class="btn btn-primary mb-3">Filter</button>
            <div class="table-container">
                <table class="table table-bordered table-hover" id="dataTable">
                    <thead class="thead-dark">
                        <tr>
                            {% for header in records[0].keys() %}
                            <th scope="col">{{ header }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in records %}
                        <tr>
                            {% for cell in row.values() %}
                            <td>{{ cell }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <script>
        function filterTable() {
            var input, filter, table, tr, td, i, j, txtValue, found;
            input = document.getElementById("filterInput");
            filter = input.value.toUpperCase();
            table = document.getElementById("dataTable");
            tr = table.getElementsByTagName("tr");

            for (i = 0; i < tr.length; i++) {
                td = tr[i].getElementsByTagName("td");
                found = false;
                for (j = 0; j < td.length; j++) {
                    if (td[j]) {
                        txtValue = td[j].textContent || td[j].innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                            found = true;
                            break; // Stop looking through the rest of the cells in this row as we found a match
                        }
                    }
                }
                if (found) {
                    tr[i].style.display = "";
                } else if (!tr[i].classList.contains('thead-dark')) { // Skip the header row for hiding
                    tr[i].style.display = "none";
                }
            }
        }
        </script>
        <!-- Bootstrap JS and dependencies -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """

    return render_template_string(table_html, records=records)

if __name__ == '__main__':
    app.run(debug=True)
