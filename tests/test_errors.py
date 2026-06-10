class TestErrorResponses:
    async def test_404_not_found(self, client):
        response = await client.get("/does-not-exist")
        assert response.status_code == 404

    async def test_404_on_api_path(self, client):
        response = await client.get("/api/nonexistent")
        assert response.status_code == 404

    async def test_405_method_not_allowed(self, client):
        response = await client.put("/api/contact")
        assert response.status_code == 405

    async def test_405_on_get_to_contact(self, client):
        response = await client.get("/api/contact")
        assert response.status_code == 405

    async def test_422_on_invalid_form_data(self, client):
        response = await client.post("/api/contact", data={"invalid": "data"})
        assert response.status_code == 422

    async def test_422_on_partial_data(self, client):
        response = await client.post("/api/contact", data={"name": "John"})
        assert response.status_code == 422

    async def test_429_rate_limit(self, client_with_rate_limit):
        for _ in range(5):
            resp = await client_with_rate_limit.post(
                "/api/contact",
                data={
                    "name": "Test",
                    "email": "test@test.com",
                    "subject": "Test",
                    "message": "Test",
                },
            )
            assert resp.status_code == 200
        response = await client_with_rate_limit.post(
            "/api/contact",
            data={
                "name": "Test",
                "email": "test@test.com",
                "subject": "Test",
                "message": "Test",
            },
        )
        assert response.status_code == 429
        data = response.json()
        assert "detail" in data

    async def test_error_response_structure(self, client):
        response = await client.post("/api/contact", data={"name": ""})
        assert response.status_code == 422
        data = response.json()
        assert "ok" in data
        assert data["ok"] is False
        assert "errors" in data
        assert isinstance(data["errors"], list)
