from auth.app.depends.gateways import (
    NotificationsManager as NotificationsManager,
)
from auth.app.depends.gateways import RMQManager as RMQManager
from auth.app.depends.gateways import (
    UsersManagementClientManager as UsersManagementClientManager,
)
from auth.app.depends.gateways import (
    UsersManagementV1Gateway as UsersManagementV1Gateway,
)
from auth.app.depends.providers import APIAccessProvider as APIAccessProvider
from auth.app.depends.providers import JWTProvider as JWTProvider
from auth.app.depends.providers import PassProvider as PassProvider
from auth.app.depends.repositories import (
    UsersSQLRepository as UsersSQLRepository,
)
from auth.app.depends.services import AuthService as AuthService
from auth.app.depends.services import (
    NotificationsService as NotificationsService,
)
from auth.app.depends.use_cases import AuthUseCase as AuthUseCase
