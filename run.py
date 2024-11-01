from app import app
from os import getenv
from dotenv import load_dotenv

load_dotenv()
#app.secret_key = getenv('SECRET_KEY', 'default_secret_key')
#print(f"Loaded SECRET_KEY: {app.secret_key}")
if __name__ == "__main__":
    app.run(debug=True)
