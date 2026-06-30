class TestHtmlRoutes:
    async def test_index_page(self, client):
        response = await client.get("/")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "Nithin Dharavath" in response.text
        assert "Backend Developer" in response.text
        assert "Contact" in response.text
        assert "Projects" in response.text

    async def test_skills_page(self, client):
        response = await client.get("/skills")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "Skills" in response.text
        assert "Nithin Dharavath" in response.text

    async def test_privacy_page(self, client):
        response = await client.get("/privacy")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "Privacy" in response.text or "privacy" in response.text.lower()

    async def test_terms_page(self, client):
        response = await client.get("/terms")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "Terms" in response.text or "terms" in response.text.lower()

    async def test_404_not_found(self, client):
        response = await client.get("/nonexistent-route")
        assert response.status_code == 404

    async def test_index_html_has_meta_tags(self, client):
        response = await client.get("/")
        assert 'name="description"' in response.text
        assert 'property="og:title"' in response.text
        assert 'name="twitter:card"' in response.text

    async def test_routes_return_different_content(self, client):
        index_resp = await client.get("/")
        skills_resp = await client.get("/skills")
        assert index_resp.text != skills_resp.text
