from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime


from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(
    limit: int,
    offset: int,
    firstname: str,
    lastname: str,
    email: str,
    birthdays: bool,
    db: Session,
):
    contacts = db.query(Contact)
    if firstname:
        contacts = contacts.filter(Contact.firstname == firstname)
    if lastname:
        contacts = contacts.filter(Contact.lastname == lastname)
    if email:
        contacts = contacts.filter(Contact.email == email)
    if birthdays:
        return get_birthdays_per_week(contacts.limit(limit).offset(offset).all())
    else:
        return contacts.limit(limit).offset(offset).all()


async def get_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create_contact(body: Contact, db: Session):
    contact = db.query(Contact).filter_by(email=body.email).first()
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is exist!"
        )
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


async def update_contact(body: ContactModel, contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.born_date = body.born_date
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


def get_birthdays_per_week(employees: list) -> None:
    current_datetime = datetime.now()
    current_year = current_datetime.year
    result = list()
    for employee in employees:
        birthday = employee.born_date
        birthday = (
            birthday.replace(year=current_year)
            if birthday.month != 1
            else birthday.replace(year=current_year + 1)
        )
        if 0 <= (birthday - current_datetime).days < 7:
            birthday_weekday = birthday.weekday()
            if birthday_weekday == 5:
                result.append(employee)
            elif birthday_weekday == 6:
                result.append(employee)
            else:
                result.append(employee)

    return result
