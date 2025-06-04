from datetime import datetime
from typing import Optional
from constants.session import DeviceType
from pydantic import BaseModel


class SessionBase(BaseModel):
    device: DeviceType
    name: Optional[str]
    city: Optional[str]


class SessionCreateDB(SessionBase):
    jwt_token: str
    user_id: int


class SessionCreate(SessionCreateDB):
    pass


class SessionUpdateDB(BaseModel):
    pass


class SessionResponse(SessionBase):
    id: int
    created_at: datetime
