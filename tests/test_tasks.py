def test_create_task(client, auth_headers):
    response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Learn pytest",
            "description": "Practice FastAPI testing",
            "status": "pending",
            "priority": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn pytest"
    assert data["description"] == "Practice FastAPI testing"
    assert data["status"] == "pending"
    assert data["priority"] == "high"

def test_create_task_requires_authentication(client):
    response = client.post(
        "/api/tasks",
        json={
            "title": "Unauthorized task",
        },
    )

    assert response.status_code == 401

def test_user_cannot_access_another_users_task(
    client,
    db,
    auth_headers,
):
    response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Private task",
        },
    )

    assert response.status_code == 201

    task_id = response.json()["id"]