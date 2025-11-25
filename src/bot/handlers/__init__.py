from aiogram import Router

from .common import router as common_router
from .search import router as search_router
from .catalog import router as catalog_router

# Создание общего роутера, чтобы потом подключить его в main
handlers_router = Router()
handlers_router.include_routers(
    search_router,
    catalog_router,
    common_router,
)
