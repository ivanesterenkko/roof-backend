from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
    HTTPException,
    status,
)

from schemas.auth import RegisterAdminData, TokenResponse, UserAuth
from utilities.exceptions import IncorrectLoginOrPasswordException
from security.auth import create_access_token
from schemas.user import UserResponse
from services.auth import (
    authenticate_user,
    create_new_session,
    delete_session,
    get_token,
    register_company,
    register_user,
)
from utilities.exceptions import ObjectAlreadyExistsError
from utilities.session import get_session_data


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(create_data: RegisterAdminData):
    try:
        company = await register_company(create_data.company)
        return await register_user(
            data=create_data.user, company_id=company.id
        )
    except ObjectAlreadyExistsError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ex.message
        ) from ex


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login_user(
    request: Request, user_data: UserAuth, response: Response
):
    user = await authenticate_user(user_data)
    if not user:
        raise IncorrectLoginOrPasswordException
    session_data = get_session_data(request)
    access_token = create_access_token({"sub": str(user.id)})
    await create_new_session(
        data=session_data,
        token=access_token,
        user_id=user.id,
    )
    response.set_cookie("access_token", access_token, httponly=True)
    return TokenResponse(access_token=access_token)


@router.post("/logout")
async def logout_user(
    response: Response,
    token: str = Depends(get_token),
):
    await delete_session(token=token)
    response.delete_cookie("access_token")
