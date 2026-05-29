import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

# storing it rather than adding it to every single test
# using this cuz, we have all the endpoint async
pytestmark=pytest.mark.asyncio


async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response=await ac.get("/")

    assert response.status_code==200
    assert "app" in response.json()

async def test_create_application():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
     response=await ac.post("/applications/",json={
        "user_id": "test@example.com",
        "company": "Google",
        "role": "Data Scientist",
        "status": "applied",
        "source": "LinkedIn",
        "notes": "Test application"
     })
    assert response.status_code==201
    assert "id" in response.json()

async def test_get_all_application():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response=await ac.get("/applications/")
    assert response.status_code==200
    assert isinstance(response.json(),list)

async def test_get_application_by_id():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # create first
        create = await ac.post("/applications/", json={
            "user_id": "test@example.com",
            "company": "Google",
            "role": "Data Scientist",
            "status": "applied",
            "source": "LinkedIn",
            "notes": "Test"
        })
        app_id = create.json()["id"]
        # then get
        response = await ac.get(f"/applications/{app_id}")
    assert response.status_code == 200
    assert "company" in response.json()


async def test_update_application():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create = await ac.post("/applications/", json={
            "user_id": "test@example.com",
            "company": "Google",
            "role": "Data Scientist",
            "status": "applied",
            "source": "LinkedIn",
            "notes": "Test"
        })
        app_id = create.json()["id"]
        response = await ac.put(f"/applications/{app_id}", json={
            "user_id": "test@example.com",
            "company": "Google",
            "role": "Data Scientist",
            "status": "interview_scheduled"
        })
    assert response.status_code == 200
    assert response.json()["status"] == "interview_scheduled"


async def test_delete_application():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create = await ac.post("/applications/", json={
            "user_id": "test@example.com", 
            "company": "Google",
            "role": "Data Scientist",
            "status": "applied",
            "source": "LinkedIn",
            "notes": "Test"
        })
        app_id = create.json()["id"]
        response = await ac.delete(f"/applications/{app_id}")
    assert response.status_code == 204
async def test_email_process():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/emails/process", json={
            "subject": "We regret to inform you",
            "body": "Dear Vamshi, after careful review we are unable to move forward with your application at this time.",
            "sender": "recruiting@company.com"
        })
    assert response.status_code == 201
    assert "predicted_status" in response.json()

async def test_analytics_summary():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/analytics/summary")
    assert response.status_code == 200
    assert "total" in response.json()