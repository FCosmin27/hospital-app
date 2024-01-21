from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Enum
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email = Column(String(70), unique=True, index=True)
    hashed_password = Column(String(70))
    is_active = Column(Boolean, default=True)

    roles = relationship('Roles', secondary='user_roles', back_populates='users')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "roles": [role.name for role in self.roles]
        }
    
class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum('admin', 'doctor', 'patient'))

    users = relationship('Users', secondary='user_roles', back_populates='roles')
    
user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

