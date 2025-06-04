from pydantic import BaseModel


class CompanyBase(BaseModel):
    title: str
    inn: str
    ogrn: str


class CompanyCreateDB(CompanyBase):
    pass


class CompanyCreate(CompanyCreateDB):
    pass


class CompanyUpdateDB(BaseModel):
    pass


class CompanyResponse(CompanyBase):
    id: int
