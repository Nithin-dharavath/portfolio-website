class TestStaticFiles:
    async def test_css_style_served(self, client):
        response = await client.get("/static/css/style.css")
        assert response.status_code == 200
        assert response.headers["content-type"] in (
            "text/css",
            "text/css; charset=utf-8",
        )

    async def test_css_skills_served(self, client):
        response = await client.get("/static/css/skills.css")
        assert response.status_code == 200
        assert "text/css" in response.headers["content-type"]

    async def test_css_privacy_served(self, client):
        response = await client.get("/static/css/privacy.css")
        assert response.status_code == 200

    async def test_css_terms_served(self, client):
        response = await client.get("/static/css/terms.css")
        assert response.status_code == 200

    async def test_js_main_served(self, client):
        response = await client.get("/static/js/main.js")
        assert response.status_code == 200
        assert "javascript" in response.headers["content-type"]

    async def test_js_skills_served(self, client):
        response = await client.get("/static/js/skills.js")
        assert response.status_code == 200

    async def test_pdf_resume_served(self, client):
        response = await client.get("/static/resume/Nitin_Dharavathu_Resume.pdf")
        assert response.status_code == 200
        assert "application/pdf" in response.headers["content-type"]

    async def test_static_file_not_found(self, client):
        response = await client.get("/static/css/nonexistent.css")
        assert response.status_code == 404

    async def test_static_file_not_found_js(self, client):
        response = await client.get("/static/js/nonexistent.js")
        assert response.status_code == 404

    async def test_static_directory_traversal_blocked(self, client):
        response = await client.get("/static/../.env")
        assert response.status_code in (400, 404)

    async def test_favicon_not_configured(self, client):
        response = await client.get("/favicon.ico")
        assert response.status_code == 404
