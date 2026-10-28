import os

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from .database import get_db
from .models import Booking, Event, User, WishlistItem
from .schemas import BookingCreate, BookingOut, EventOut, LoginInput, UserCreate, UserOut, WishlistCreate
from .security import COOKIE_NAME, create_session, hash_password, read_session, verify_password

router = APIRouter(prefix="/api")
COOKIE_SECURE = os.getenv("HAPA_COOKIE_SECURE", "false").lower() == "true"


def current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get(COOKIE_NAME)
    user_id = read_session(token) if token else None
    user = db.get(User, user_id) if user_id else None
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please log in to continue")
    return user


def set_session(response: Response, user: User) -> None:
    response.set_cookie(COOKIE_NAME, create_session(user.id), httponly=True, secure=COOKIE_SECURE, samesite="lax", max_age=7*24*60*60, path="/")


@router.post("/auth/signup", response_model=dict, status_code=201)
def signup(payload: UserCreate, response: Response, db: Session = Depends(get_db)):
    email = str(payload.email).lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(name=payload.name, email=email, password_hash=hash_password(payload.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="An account with this email already exists") from None
    db.refresh(user)
    set_session(response, user)
    return {"user": UserOut.model_validate(user)}


@router.post("/auth/login", response_model=dict)
def login(payload: LoginInput, response: Response, db: Session = Depends(get_db)):
    email = str(payload.email).lower()
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect")
    set_session(response, user)
    return {"user": UserOut.model_validate(user)}


@router.get("/auth/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user


@router.post("/auth/logout", status_code=204)
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME, path="/", httponly=True, secure=COOKIE_SECURE, samesite="lax")


@router.get("/events", response_model=list[EventOut])
def events(db: Session = Depends(get_db)):
    return db.scalars(select(Event).order_by(Event.starts_at, Event.id)).all()


@router.get("/me/wishlist", response_model=list[EventOut])
def get_wishlist(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Event).join(WishlistItem).where(WishlistItem.user_id == user.id).order_by(WishlistItem.created_at.desc())).all()


@router.post("/me/wishlist", response_model=EventOut, status_code=201)
def add_wishlist(payload: WishlistCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    event = db.get(Event, payload.event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    exists = db.scalar(select(WishlistItem).where(WishlistItem.user_id == user.id, WishlistItem.event_id == event.id))
    if not exists:
        db.add(WishlistItem(user_id=user.id, event_id=event.id))
        db.commit()
    return event


@router.delete("/me/wishlist/{event_id}", status_code=204)
def remove_wishlist(event_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(WishlistItem).where(WishlistItem.user_id == user.id, WishlistItem.event_id == event_id))
    if item:
        db.delete(item)
        db.commit()


@router.get("/me/bookings", response_model=list[BookingOut])
def get_bookings(user: User = Depends(current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(Booking).options(joinedload(Booking.event)).where(Booking.user_id == user.id).order_by(Booking.created_at.desc())).all()
    return [{"id": row.id, "event": row.event, "quantity": row.quantity, "note": row.note, "created_at": row.created_at} for row in rows]


@router.post("/me/bookings", response_model=BookingOut, status_code=201)
def add_booking(payload: BookingCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    event = db.get(Event, payload.event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    row = Booking(user_id=user.id, event_id=event.id, quantity=payload.quantity, note=payload.note.strip() or None)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "event": event, "quantity": row.quantity, "note": row.note, "created_at": row.created_at}
