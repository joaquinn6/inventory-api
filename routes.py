"""Archivo de routes"""
from fastapi import APIRouter

from controllers import users_controller
from controllers import product_controller
from controllers import config_controller
from controllers import supplier_controller
from controllers import purchase_controller
router = APIRouter()
router.include_router(config_controller.router)
router.include_router(users_controller.router)
router.include_router(product_controller.router)
router.include_router(supplier_controller.router)
router.include_router(purchase_controller.router)
