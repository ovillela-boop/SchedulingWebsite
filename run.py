from app import create_app
from app.models import db

print("starting run.py")

app = create_app()
print("app created")

if __name__ == '__main__':
    print("inside main block")
    with app.app_context():
        db.create_all()
        print("db created")
    print("starting flask")
    app.run(debug=True, use_reloader=False)