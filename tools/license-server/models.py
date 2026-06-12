import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    licenses = relationship("License", back_populates="user")

class License(Base):
    __tablename__ = "licenses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_key = Column(String, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tier = Column(String, nullable=False)
    max_machines = Column(Integer, default=1)
    issued_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    revoked = Column(Boolean, default=False)
    metadata = Column(JSON, default=dict)
    user = relationship("User", back_populates="licenses")
    activations = relationship("Activation", back_populates="license")

class Machine(Base):
    __tablename__ = "machines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fingerprint = Column(String, nullable=False)
    hostname = Column(String)
    platform = Column(String)
    first_seen = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_seen = Column(DateTime(timezone=True), default=datetime.utcnow)
    activations = relationship("Activation", back_populates="machine")

class Activation(Base):
    __tablename__ = "activations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_id = Column(UUID(as_uuid=True), ForeignKey("licenses.id", ondelete="CASCADE"))
    machine_id = Column(UUID(as_uuid=True), ForeignKey("machines.id", ondelete="CASCADE"))
    token = Column(Text, nullable=False)
    activated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_verified = Column(DateTime(timezone=True), default=datetime.utcnow)
    active = Column(Boolean, default=True)
    license = relationship("License", back_populates="activations")
    machine = relationship("Machine", back_populates="activations")
