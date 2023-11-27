from typing import Optional, List
from pydantic import BaseModel, EmailStr


class TokenRequestForm(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None


class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: str


class UserCreate(UserBase):
    firstName: str
    lastName: str
    password: str


class UserUpdate(UserBase):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class Patient(BaseModel):
    lastName: str
    firstName: str
    middleName: str
    countryCode: str
    street: str
    streetExtended: str
    city: str
    state: str
    postCode: str
    phoneNumberHome: str
    email: str
    phoneNumberCell: str


class Insurance(BaseModel):
    insuranceType: str
    insuranceCompanyName: str
    insuranceCompanyPhoneNumber: str
    insuranceCompanyAddress: str
    insuranceCompanyCity: str
    insuranceCompanyState: str
    insuranceCompanyZip: str
    relationshipLastName: str
    relationshipFirstName: str
    relationshipMiddleName: str
    relationshipToPatient: str
    relationshipStreetAddress: str
    relationshipCity: str
    relationshipState: str
    relationshipZip: str


class Invoice(BaseModel):
    date: str
    code: str
    modifier: str
    icd10: str


class Document(BaseModel):
    dbName: str
    ex_pid: str
    Patient: Patient
    Insurance: List[Insurance]
    Invoice: List[Invoice]


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
