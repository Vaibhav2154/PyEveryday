from fastapi import exceptions, status, APIRouter
from backend.routers.auth.schema import UserCreate
auth_router = APIRouter()

@auth_router.post('/Signup', status_code=status.HTTP_201_CREATED)
async def create_user(user_data:UserCreate):
    pass