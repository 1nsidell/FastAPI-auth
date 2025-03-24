from typing import Dict

from auth.settings import settings

users_management_headers: Dict = {
    "X-API-Key": settings.api_key,
}
