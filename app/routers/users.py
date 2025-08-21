from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/users", tags=["users"])

# Modelos Pydantic
class UserBase(BaseModel):
    email: str
    full_name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Base de datos simulada (en un proyecto real usarías SQLAlchemy)
users_db = []
user_id_counter = 1

@router.get("/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 100):
    """
    Obtener lista de usuarios
    """
    return users_db[skip : skip + limit]

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """
    Obtener un usuario específico por ID
    """
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Crear un nuevo usuario
    """
    global user_id_counter
    
    # Verificar si el email ya existe
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email ya registrado")
    
    new_user = {
        "id": user_id_counter,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "created_at": datetime.now()
    }
    
    users_db.append(new_user)
    user_id_counter += 1
    
    return new_user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    """
    Actualizar un usuario existente
    """
    for user in users_db:
        if user["id"] == user_id:
            update_data = user_update.dict(exclude_unset=True)
            user.update(update_data)
            return user
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """
    Eliminar un usuario
    """
    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db.pop(i)
            return
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
