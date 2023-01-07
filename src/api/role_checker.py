from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from auth_helpers import *


def role_is_at_least(user, role):
    roles = {"user": 0, "contributor": 1, "editor": 2, "admin": 3}
    return roles[user.role] >= roles[role]


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        if user.role not in self.allowed_roles:
            print(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")


allow_create_resource = RoleChecker(["admin"])
allow_edit_resource = RoleChecker(["editor", "admin"])
allow_contribute_resource = RoleChecker(["admin", "editor", "contributor"])
