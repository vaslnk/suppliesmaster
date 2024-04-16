from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    # Enhanced HTML with Bootstrap for styling, with JavaScript to change iframe content and highlight active link
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
            .iframe-container { 
                position: relative;
                overflow: hidden;
                width: 100%;
                padding-top: 56.25%; /* 16:9 Aspect Ratio */
            }
            .iframe-container iframe {
                position: absolute;
                top: 0;
                left: 0;
                bottom: 0;
                right: 0;
                width: 100%;
                height: 100%;
                border: none;
            }
            .nav-link {
                cursor: pointer;
            }
            .nav-link.active {
                font-weight: bold;
                color: navy; /* Highlight color for the current page */
            }
        </style>
        <script>
            function changeIframe(url, element) {
                // Update iframe source
                document.getElementById('main-iframe').src = url;
                // Remove active class from all links
                document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
                // Add active class to the clicked link
                element.classList.add('active');
            }
        </script>
    </head>
    <body>
        <div class="container-fluid">
            <h2 class="my-4">Suppliers Data</h2>
            <!-- Navigation Links -->
            <div class="nav mb-3">
                <a onclick="changeIframe('http://localhost/public/grid/drwX450lPian4lwKqyaj5WxqO2Sj1Xv0AYnkaZ6ydTQ', this)" class="nav-link active">⏰ Supplier Tracker</a>
                <a onclick="changeIframe('http://localhost/form/05yM-256TOWVGMe4FtPCwm6TOs7UYknsyRXAYy0I9Cw', this)" class="nav-link">📥 Add a Supplier</a>
            </div>
            <!-- Divider line -->
            <hr>
            <div class="iframe-container">
                <iframe id="main-iframe" src="http://localhost/public/grid/drwX450lPian4lwKqyaj5WxqO2Sj1Xv0AYnkaZ6ydTQ" frameborder="0"></iframe>
            </div>
        </div>
        <!-- Bootstrap JS and dependencies -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """

    return table_html

if __name__ == '__main__':
    app.run(debug=True)
