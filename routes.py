from flask import request, jsonify, abort
from flask_restful import Resource
from functools import wraps
from .models import BlacklistEntry, db
from .schemas import BlacklistSchema

schema = BlacklistSchema()

STATIC_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImlhdCI6MTcwODk5NjAwMCwiZXhwIjoxNzM5NTMyMDAwfQ.vbJPj04SRQfQBoDh-Z_T70F9R50wF1BuFbUKvUFn1Hk"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "")
        if token != f"Bearer {STATIC_TOKEN}":
            abort(401)
        return f(*args, **kwargs)
    return decorated

class BlacklistResource(Resource):
    @token_required
    def post(self):
        print("✅ POST /blacklists endpoint alcanzado")
        data = request.get_json()
        print(f"📩 Payload recibido: {data}")
        errors = schema.validate(data)
        if errors:
            print(f"⚠️ Errores de validación: {errors}")
            return {"errors": errors}, 400
        try:
            new_entry = BlacklistEntry(
                email=data['email'],
                app_uuid=data['app_uuid'],
                blocked_reason=data.get('blocked_reason'),
                ip_address=request.remote_addr
            )
            print(f"🆕 Instancia creada: {new_entry}")
            db.session.add(new_entry)
            print("📥 Registro agregado a la sesión")
            db.session.commit()
            print("💾 Commit exitoso a la base de datos")
            return {"message": "Email added to blacklist"}, 201
        except Exception as e:
            print(f"❌ Error al agregar a la base de datos: {e}")
            db.session.rollback()
            return {"error": "Failed to add email to blacklist"}, 500

class BlacklistCheckResource(Resource):
    @token_required
    def get(self, email):
        entry = BlacklistEntry.query.filter_by(email=email).first()
        if entry:
            return {"blacklisted": True, "reason": entry.blocked_reason}, 200
        return {"blacklisted": False}, 200
    
class HealthCheck(Resource):
    def get(self):
        return {"status": "ok"}, 200


def register_routes(api):
    api.add_resource(BlacklistResource, '/blacklists')
    api.add_resource(BlacklistCheckResource, '/blacklists/<string:email>')
    api.add_resource(HealthCheck, '/health')
