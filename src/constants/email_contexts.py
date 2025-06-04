from typing import TypedDict


class LinkContext(TypedDict):
    url: str


class EmailContext(TypedDict):
    email: str


class PasswordContext(TypedDict):
    password: str


class UserAddedToCompanyContext(LinkContext, EmailContext, PasswordContext):
    company_name: str
