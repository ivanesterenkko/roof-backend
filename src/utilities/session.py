from fastapi import Request
from user_agents import parse

from schemas.session import SessionBase
from constants.session import DeviceType


def get_session_data(data: Request) -> SessionBase:
    user_agent = parse(data.headers.get("user-agent", ""))
    device_type = DeviceType.desktop
    if user_agent.is_mobile:
        device_type = DeviceType.mobile
    if user_agent.is_tablet:
        device_type = DeviceType.tablet
    name = user_agent.device.model if user_agent.device.model else None
    city = None
    return SessionBase(
        device=device_type,
        name=name,
        city=city,
    )
