"""API endpoint tests for SORA module."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_calculate_sora(client: AsyncClient):
    payload = {
        "mtom_kg": 2.0,
        "characteristic_dimension_m": 0.5,
        "max_speed_ms": 20.0,
        "max_population_density": 100.0,
        "flight_altitude_m": 50.0,
        "airspace_class": "G",
        "country_code": "NO",
    }
    response = await client.post("/api/v1/sora/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "intrinsic_grc" in data
    assert "sail_level" in data
    assert "oso_requirements" in data
    assert len(data["oso_requirements"]) == 24


@pytest.mark.asyncio
async def test_calculate_grc(client: AsyncClient):
    payload = {
        "characteristic_dimension_m": 0.5,
        "max_speed_ms": 20.0,
        "max_population_density": 100.0,
    }
    response = await client.post("/api/v1/sora/grc", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intrinsic_grc"] == 3


@pytest.mark.asyncio
async def test_calculate_arc(client: AsyncClient):
    payload = {
        "flight_altitude_m": 50.0,
        "airspace_class": "G",
    }
    response = await client.post("/api/v1/sora/arc", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["initial_arc"] == "ARC-b"


@pytest.mark.asyncio
async def test_get_sail_matrix(client: AsyncClient):
    response = await client.get("/api/v1/sora/sail-matrix")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 28  # 7 GRC levels × 4 ARC levels


@pytest.mark.asyncio
async def test_list_osos(client: AsyncClient):
    response = await client.get("/api/v1/sora/osos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 24


@pytest.mark.asyncio
async def test_validation_error_no_drone_specs(client: AsyncClient):
    payload = {
        "max_population_density": 100.0,
        "flight_altitude_m": 50.0,
        "airspace_class": "G",
    }
    response = await client.post("/api/v1/sora/calculate", json=payload)
    assert response.status_code == 422  # Validation error
