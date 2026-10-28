from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

NameText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=100)]
PasswordText = Annotated[str, StringConstraints(min_length=10, max_length=128)]


class UserCreate(BaseModel):
    name: NameText
    email: EmailStr
    password: PasswordText


class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    slug: str
    title: str
    artist: str
    city: str
    venue: str
    starts_at: datetime
    price_from_kes: int | None
    genre: str
    source_url: str
    source_label: str
    art: str
    featured: bool


class WishlistCreate(BaseModel):
    event_id: int


class BookingCreate(BaseModel):
    event_id: int
    quantity: int = Field(default=1, ge=1, le=10)
    note: str = Field(default="", max_length=240)


class BookingOut(BaseModel):
    id: int
    event: EventOut
    quantity: int
    note: str | None
    created_at: datetime
