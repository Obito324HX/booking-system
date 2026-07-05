from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402  (must load .env before app config reads env vars)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
