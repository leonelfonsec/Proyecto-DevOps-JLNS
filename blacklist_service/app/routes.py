from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .models import BlacklistEntry, db
from .schemas import BlacklistSchema

schema = BlacklistSchema()

class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        errors = schema.validate(data)
        if errors:
            return {"errors": errors}, 400

        new_entry = BlacklistEntry(
            email=data['email'],
            app_uuid=data['app_uuid'],
            blocked_reason=data.get('blocked_reason'),
            ip_address=request.remote_addr
        )
        db.session.add(new_entry)
        db.session.commit()
        return {"message": "Email added to blacklist"}, 201

class BlacklistCheckResource(Resource):
    @jwt_required()
    def get(self, email):
        entry = BlacklistEntry.query.filter_by(email=email).first()
        if entry:
            return {"blacklisted": True, "reason": entry.blocked_reason}, 200
        return {"blacklisted": False}, 200

def register_routes(api):
    api.add_resource(BlacklistResource, '/blacklists')
    api.add_resource(BlacklistCheckResource, '/blacklists/<string:email>')