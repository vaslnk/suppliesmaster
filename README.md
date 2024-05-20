# Intro
The app is running in production at the following urls:


# Setup
```shell
# Install virtualenv (if not already installed)
python3 -m pip install --user virtualenv

# setup virtual env
virtualenv venv

# activate virtualenv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

# Running the App
```shell
# Get baserow backend Docker software running in background
docker run \
  -d \
  --name baserow \
  -e BASEROW_PUBLIC_URL=http://localhost \
  -v baserow_data:/baserow/data \
  -p 80:80 \
  -p 443:443 \
  --restart unless-stopped \
  baserow/baserow:1.24.2

# for auto-reload in local dev (do not run in production)
export FLASK_ENV=development

# run the app
flask run
```
