from app import create_app
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

application = create_app()
#print(f"\n🔗 DATABASE URI en runtime: {application.config['SQLALCHEMY_DATABASE_URI']}\n")

# if __name__ == "__main__":
#     application.run(host="0.0.0.0", port=5000)