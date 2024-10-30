"""Archivo de routes"""
from fastapi import APIRouter

from controllers import users_controller
from controllers import product_controller
router = APIRouter()
router.include_router(users_controller.router)
router.include_router(product_controller.router)
