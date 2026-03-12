from fastapi import APIRouter

from app.api.v1.endpoints import caa, dma, drones, sora

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(drones.router, prefix="/drones", tags=["Drones"])
api_router.include_router(sora.router, prefix="/sora", tags=["SORA"])
api_router.include_router(caa.router, prefix="/caa", tags=["CAA Rules"])
api_router.include_router(dma.router, prefix="/dma", tags=["DMA"])
