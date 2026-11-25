def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_get_user(client):
    created = client.post("/users", json={"name": "Sara", "email": "sara@example.com"})
    assert created.status_code == 201
    user_id = created.json()["id"]
    fetched = client.get(f"/users/{user_id}")
    assert fetched.status_code == 200
    assert fetched.json()["email"] == "sara@example.com"

def test_duplicate_email_returns_conflict(client):
    body = {"name": "Sara", "email": "sara@example.com"}
    assert client.post("/users", json=body).status_code == 201
    assert client.post("/users", json=body).status_code == 409

def test_create_task_requires_existing_user(client):
    response = client.post("/tasks", json={
        "title": "Finish report", "description": "Chapter 3", "user_id": 999
    })
    assert response.status_code == 404

def test_create_and_complete_task(client):
    user = client.post("/users", json={"name": "Ali", "email": "ali@example.com"}).json()
    task = client.post("/tasks", json={"title": "Study", "user_id": user["id"]})
    assert task.status_code == 201
    task_id = task.json()["id"]
    updated = client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True
