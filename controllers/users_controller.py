"""Routes y controllers de usuarios"""
from fastapi import APIRouter, status, Body
from services.user import UserService
import core.var_mongo_provider as mongo_provider
from core.auth import generate_token

router = APIRouter(
    prefix="",
    tags=["Usuario"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def user_post(contract: dict = Body(...)):
  service = UserService(mongo_provider.db)
  return service.create_user(contract)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(contract: dict = Body(...)):
  access_token = generate_token(contract['email'], contract['password'])
  return access_token


# @router.get("")
# async def usesr_get():
#   users = mongo_provider.db.users.find({})
#   return users
#
#
# @router.put("/{id_usuario}/amigo")
# async def user_put(id_usuario: str, body: dict):
#   friend = mongo_provider.db.users.find_one(
#       {'username': body['username'].lower().strip().replace(" ", "_")})
#   user = mongo_provider.db.users.find_one({'_id': id_usuario})
#   if not 'amigos' in user:
#     user["amigos"] = []
#   if friend["username"] == user["username"] or friend["username"] in user["amigos"]:
#     raise HTTPException(403, "Usuario no valido")
#
#   if not friend:
#     raise HTTPException(409, "Usuario no existente")
#
#   user['amigos'].append(friend['username'])
#
#   mongo_provider.db.users.update_one({'_id': id_usuario}, {'$set': user})
#   return user
#
#
# @router.get("/{id_usuario}/table")
# async def table_get(id_usuario: str):
#   user = mongo_provider.db.users.find_one({'_id': id_usuario})
#   arrayTable = user['amigos'] if 'amigos' in user else []
#   arrayTable.append(user['username'])
#
#   users = mongo_provider.db.users.find(
#       {'username': {'$in': arrayTable}}).sort("total", -1)
#   return list(users)
#
#
# @router.delete("/{id_usuario}/delete")
# async def user_delete(id_usuario: str):
#   mongo_provider.db.users.delete_one({'_id': id_usuario})
#   return {'message': 'ok'}
#
