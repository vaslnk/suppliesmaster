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
            body, html {
              width: 100%; // or body { width: 960px; } if you're using a fixed width
            }
            .iframe-container { 
                position: relative;
                overflow: hidden;
                width: 100%;
                padding-top: 56.25%; /* 16:9 Aspect Ratio */
            }
            .responsive-iframe {
                position: absolute;
                top: 0;
                left: 0;
                bottom: 0;
                right: 0;
                width: 100%;
                height: 100%;
                border: none;
            }
            @media (max-width: 768px) {
                .iframe-container {
                    position: relative;
                    width: 100%;
                    height: 500px;
                }
                .responsive-iframe {
                    top: 0;
                    left: 0;
                    bottom: 0;
                    right: 0;
                    position: absolute;
                    width: 768px;
                    height: 200vw;
                    border: none;
                    transform: scale(0.5);
                    transform-origin: 0 0;
                }
            }
            .nav-link {
                cursor: pointer;
            }
            .nav-link.active {
                font-weight: bold;
                color: navy; /* Highlight color for the current page */
            }
            .nav-right {
                float: right;
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
                <a onclick="changeIframe('https://baserow.io/public/grid/4mupvSXIVPtgzNvRy7ULqoxGRw2DfFg3CUbAB9YWgRI', this)" class="nav-link active">⏰ Supplier Tracker</a>
                <a onclick="changeIframe('https://baserow.io/form/Y1MUYeYBSqhYcrSvO-7DAGhwefCCLj8B9ZY5khZGQ8U', this)" class="nav-link">📥 Add a Supplier</a>
                <a href="https://docs.google.com/spreadsheets/d/19vp-zb0XbdlpGozwSSjI6bpn_XNki_yiDQYNlqUVEK4/edit?usp=sharing" class="nav-link nav-right" target="_blank">🕵️‍♀️ Fix Incorrect Info</a>
            </div>
            <!-- Divider line -->
            <hr>
            <div class="iframe-container">
                <iframe class="responsive-iframe" id="main-iframe" src="https://baserow.io/public/grid/4mupvSXIVPtgzNvRy7ULqoxGRw2DfFg3CUbAB9YWgRI" frameborder="0"></iframe>
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
    app.run(host='0.0.0.0', port=80)
