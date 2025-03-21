"""Archivo de routes"""
from fastapi import APIRouter

from controllers import users_controller
from controllers import product_controller
from controllers import config_controller
from controllers import supplier_controller
from controllers import purchase_controller
from controllers import sale_controller
from controllers import dashboard_controller
router = APIRouter()
router.include_router(config_controller.router)
router.include_router(users_controller.router)
router.include_router(product_controller.router)
router.include_router(supplier_controller.router)
router.include_router(sale_controller.router)
router.include_router(purchase_controller.router)
router.include_router(dashboard_controller.router)
