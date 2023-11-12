from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ResponseContact
from src.repository import contacts as repository_contacts

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ResponseContact])
async def get_contacts(
    limit: int = Query(10, le=1000),
    offset: int = 0,
    firstname: str = "",
    lastname: str = "",
    email: str = "",
    birthdays: bool = False,
    db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, offset, firstname, lastname, email, birthdays, db)
    return contacts


@router.get("/{contact_id}", response_model=ResponseContact)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ResponseContact, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ResponseContact)
async def update_contact(
    body: ContactModel, contact_id: int, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(
    contact_id: int, db: Session = Depends(get_db)
):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
