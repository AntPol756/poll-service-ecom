class UserClient:
    def get_user(self, user_id: int) -> dict:
        try:
            response = requests.get(f"{settings.USER_SERVICE_URL}/users/{user_id}", timeout=5)
        except requests.RequestException as exc:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "User Service is unavailable") from exc

        if response.status_code == 404:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        if response.status_code != 200:
            raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Unexpected response from User Service")
        return response.json()

    def ensure_registered(self, user_id: int) -> None:
        if not self.get_user(user_id)["is_registered"]:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Only registered users can answer questions")