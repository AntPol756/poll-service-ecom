import requests
from fastapi import HTTPException, status

from app.config import settings


class UserClient:
    """Talks to the User Service over its REST API."""

    def get_user(self, user_id: int) -> dict:
        try:
            response = requests.get(
                f"{settings.USER_SERVICE_URL}/users/{user_id}", timeout=5
            )
        except requests.RequestException as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User Service is unavailable",
            ) from exc

        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unexpected response from User Service",
            )
        return response.json()

    def ensure_registered(self, user_id: int) -> None:
        user = self.get_user(user_id)
        if not user.get("is_registered"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only registered users can answer questions",
            )
