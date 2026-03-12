"""API endpoint tests for DMA module."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_dimensions(client: AsyncClient):
    response = await client.get("/api/v1/dma/dimensions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    codes = {d["code"] for d in data}
    assert codes == {"OPS", "TECH", "SAFE", "COMP", "HR", "DATA"}


@pytest.mark.asyncio
async def test_list_questions(client: AsyncClient):
    response = await client.get("/api/v1/dma/questions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 30  # 5 questions × 6 dimensions


@pytest.mark.asyncio
async def test_filter_questions_by_dimension(client: AsyncClient):
    response = await client.get("/api/v1/dma/questions?dimension=OPS")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert all(q["question_code"].startswith("OPS") for q in data)


@pytest.mark.asyncio
async def test_run_assessment(client: AsyncClient):
    responses = {f"OPS_0{i}": 4 for i in range(1, 6)}
    responses.update({f"TECH_0{i}": 3 for i in range(1, 6)})
    responses.update({f"SAFE_0{i}": 3 for i in range(1, 6)})
    responses.update({f"COMP_0{i}": 4 for i in range(1, 6)})
    responses.update({f"HR_0{i}": 3 for i in range(1, 6)})
    responses.update({f"DATA_0{i}": 3 for i in range(1, 6)})

    payload = {
        "organization_name": "Oslo Kommune",
        "responses": responses,
    }
    response = await client.post("/api/v1/dma/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "dimension_scores" in data
    assert "maturity_level" in data
    assert "overall_score" in data
    assert data["organization_name"] == "Oslo Kommune"
    assert data["id"] is not None  # Persisted
