import pytest
from app import create_app, db
from app.models import Task

@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    config = {"DATABASE_URI": f"sqlite:///{db_path}"}
    app = create_app(test_config=config)
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_create_and_list(client):
    rv = client.post("/api/tasks", json={"title":"Test Task", "description":"desc"})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["title"] == "Test Task"
    rv2 = client.get("/api/tasks")
    assert rv2.status_code == 200
    arr = rv2.get_json()
    assert any(t['title']=="Test Task" for t in arr)

def test_update_and_delete(client):
    rv = client.post("/api/tasks", json={"title":"To Update"})
    task = rv.get_json()
    tid = task['id']
    rv2 = client.patch(f"/api/tasks/{tid}", json={"done": True, "title":"Updated"})
    assert rv2.status_code == 200
    assert rv2.get_json()['done'] is True
    rv3 = client.delete(f"/api/tasks/{tid}")
    assert rv3.status_code == 200
    rv4 = client.get(f"/api/tasks/{tid}")
    assert rv4.status_code == 404
