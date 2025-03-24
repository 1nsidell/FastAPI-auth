from auth.app.services import AuthServiceProtocol, NotificationsServiceProtocol
from auth.app.use_cases import AuthUseCaseProtocol
from auth.core.schemas import SBaseSignIn, SBaseSignUp, TokenInfo


class AuthUseCaseImpls(AuthUseCaseProtocol):
    def __init__(
        self,
        auth_service: AuthServiceProtocol,
        notifications_service: NotificationsServiceProtocol,
    ):
        self.auth_service = auth_service
        self.notifications_service = notifications_service

    async def signup(self, data: SBaseSignUp) -> TokenInfo:
        user_session, user_info = await self.auth_service.register_user(data)
        await self.notifications_service.send_confirm_email(
            data.email, user_info
        )
        return user_session

    async def signin(self, data: SBaseSignIn) -> TokenInfo:
        user_session = await self.auth_service.authenticate_user(data)
        return user_session
