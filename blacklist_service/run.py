from app import create_app

app = create_app()
print(f"\n🔗 DATABASE URI en runtime: {app.config['SQLALCHEMY_DATABASE_URI']}\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)