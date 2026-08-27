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

def test_get_tasks(client, auth_headers):
    client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Task One",
            "status": "pending",
            "priority": "low",
        },
    )

    client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Task Two",
            "status": "completed",
            "priority": "high",
        },
    )

    response = client.get(
        "/api/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2

def test_get_task(client, auth_headers):
    create_response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Learn HTTPX",
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Learn HTTPX"

def test_get_nonexistent_task(client, auth_headers):
    response = client.get(
        "/api/tasks/99999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_update_task(client, auth_headers):
    create_response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Original title",
            "priority": "low",
        },
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/api/tasks/{task_id}",
        headers=auth_headers,
        json={
            "title": "Updated title",
            "priority": "high",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated title"
    assert data["priority"] == "high"

def test_delete_task(client, auth_headers):
    create_response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Task to delete",
        },
    )

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/api/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 204
    assert response.content == b""

def test_create_task_validation(client, auth_headers):
    response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Hi",
        },
    )

    assert response.status_code == 422

def test_invalid_task_status(client, auth_headers):
    response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Valid title",
            "status": "banana",
        },
    )

    assert response.status_code == 422

def test_get_tasks_requires_authentication(client):
    response = client.get(
        "/api/tasks",
    )

    assert response.status_code == 401

def test_user_cannot_access_another_users_task(
    client,
    auth_headers,
    second_auth_headers,
):
    create_response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Private task",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/tasks/{task_id}",
        headers=second_auth_headers,
    )

    assert response.status_code == 404

def test_task_pagination(client, auth_headers):
    for i in range(5):
        response = client.post(
            "/api/tasks",
            headers=auth_headers,
            json={
                "title": f"Task {i}",
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/api/tasks?page=1&limit=2",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["total"] == 5
    assert data["pages"] == 3
    assert len(data["items"]) == 2

def test_last_pagination_page(client, auth_headers):
    for i in range(5):
        client.post(
            "/api/tasks",
            headers=auth_headers,
            json={
                "title": f"Task {i}",
            },
        )

    response = client.get(
        "/api/tasks?page=3&limit=2",
        headers=auth_headers,
    )

    data = response.json()

    assert data["page"] == 3
    assert len(data["items"]) == 1

def test_filter_tasks_by_status(client, auth_headers):
    client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Pending task",
            "status": "pending",
        },
    )

    client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "title": "Completed task",
            "status": "completed",
        },
    )

    response = client.get(
        "/api/tasks?status=completed",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["status"] == "completed"

