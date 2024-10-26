"""Archivo de routes"""
from fastapi import APIRouter

from controllers import users_controller

router = APIRouter()
router.include_router(users_controller.router)
