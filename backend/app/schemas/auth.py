from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request with username and password."""
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    is_default_admin: bool = False  # Indicates if this is the default admin (needs setup)


class TokenData(BaseModel):
    """Data encoded in JWT token."""
    username: str


class InitialSetupRequest(BaseModel):
    """Request to create a new admin account during initial setup."""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    full_name: Optional[str] = ""


class PasswordResetRequest(BaseModel):
    """Request a password reset email."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Confirm password reset with token and new password."""
    token: str
    new_password: str = Field(..., min_length=6, max_length=100)


class SystemStatusResponse(BaseModel):
    """System initialization status."""
    needs_setup: bool
    message: str
