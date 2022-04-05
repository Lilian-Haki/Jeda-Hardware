from models.Role import Role
from main import db

def seeding():
    roles = ['Admin', 'Medical Staff', 'Nurse', 'Lab Technician']

    for role in roles:        
        exists = Role.query.filter_by(name = role).first()

        if not exists:
            new_role = Role(name = role)
            db.session.add(new_role)
            db.session.commit()