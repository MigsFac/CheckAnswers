from app import create_app
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
