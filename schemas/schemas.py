from typing import Optional, List
from pydantic import BaseModel, EmailStr


class TokenRequestForm(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    first_name: str
    last_name: str
    password: str


class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
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


class OpenAIResponse(BaseModel):
    Determination: str
    Reasoning: str
    Query: str
    Context: Optional[str]
    Raw_Output: str


class PostalAddress(BaseModel):
    revision: int
    regionCode: str
    languageCode: str
    postalCode: str
    sortingCode: str
    administrativeArea: str
    locality: str
    sublocality: str
    addressLines: List[str]
    recipients: List[str]
    organization: str


class LanguageOptions(BaseModel):
    returnEnglishLatinAddress: bool


class AddressValidation(BaseModel):
    address: PostalAddress
    previousResponseId: str
    enableUspsCass: bool
    languageOptions: LanguageOptions


class Config:
    allow_mutation = True
