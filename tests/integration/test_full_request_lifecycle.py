class TestFullRequestLifecycle:
    async def test_homepage_to_contact_flow(self, client):
        home = await client.get("/")
        assert home.status_code == 200

        contact_resp = await client.post(
            "/api/contact",
            data={
                "name": "Alice",
                "email": "alice@example.com",
                "subject": "Partnership",
                "message": "Let's work together on a project.",
            },
        )
        assert contact_resp.status_code == 200
        assert contact_resp.json()["ok"] is True

    async def test_browse_skills_then_contact(self, client):
        skills = await client.get("/skills")
        assert skills.status_code == 200
        assert "Skills" in skills.text

        contact_resp = await client.post(
            "/api/contact",
            data={
                "name": "Bob",
                "email": "bob@example.com",
                "subject": "Question",
                "message": "I have a question about your services.",
            },
        )
        assert contact_resp.status_code == 200
        assert contact_resp.json()["ok"] is True

    async def test_invalid_form_then_valid(self, client):
        bad_resp = await client.post(
            "/api/contact",
            data={"name": "", "email": "bad", "subject": "", "message": ""},
        )
        assert bad_resp.status_code == 422

        good_resp = await client.post(
            "/api/contact",
            data={
                "name": "Charlie",
                "email": "charlie@example.com",
                "subject": "Hello",
                "message": "Hi there!",
            },
        )
        assert good_resp.status_code == 200
        assert good_resp.json()["ok"] is True

    async def test_privacy_policy_page(self, client):
        privacy = await client.get("/privacy")
        assert privacy.status_code == 200

        terms = await client.get("/terms")
        assert terms.status_code == 200

    async def test_page_navigation_links_exist(self, client):
        home = await client.get("/")
        links = [
            "/",
            "/skills",
            "/privacy",
            "/terms",
        ]
        for link in links:
            assert link in home.text or f'href="{link}"' in home.text
