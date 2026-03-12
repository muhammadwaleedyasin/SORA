import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.drone import DroneModel
from app.schemas.drone import DroneModelCreate, DroneModelResponse, DroneModelUpdate

router = APIRouter()


@router.get("/", response_model=list[DroneModelResponse])
async def list_drones(
    skip: int = 0,
    limit: int = 50,
    manufacturer: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List drone models with optional filtering."""
    query = select(DroneModel).offset(skip).limit(limit)
    if manufacturer:
        query = query.where(DroneModel.manufacturer.ilike(f"%{manufacturer}%"))
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=DroneModelResponse, status_code=201)
async def create_drone(drone: DroneModelCreate, db: AsyncSession = Depends(get_db)):
    """Register a new drone model."""
    db_drone = DroneModel(**drone.model_dump())
    db.add(db_drone)
    await db.commit()
    await db.refresh(db_drone)
    return db_drone


@router.get("/{drone_id}", response_model=DroneModelResponse)
async def get_drone(drone_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get a drone model by ID."""
    result = await db.execute(select(DroneModel).where(DroneModel.id == drone_id))
    drone = result.scalar_one_or_none()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone model not found")
    return drone


@router.put("/{drone_id}", response_model=DroneModelResponse)
async def update_drone(
    drone_id: uuid.UUID,
    update: DroneModelUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a drone model."""
    result = await db.execute(select(DroneModel).where(DroneModel.id == drone_id))
    drone = result.scalar_one_or_none()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone model not found")

    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(drone, field, value)

    await db.commit()
    await db.refresh(drone)
    return drone


@router.delete("/{drone_id}", status_code=204)
async def delete_drone(drone_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete a drone model."""
    result = await db.execute(select(DroneModel).where(DroneModel.id == drone_id))
    drone = result.scalar_one_or_none()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone model not found")
    await db.delete(drone)
    await db.commit()
