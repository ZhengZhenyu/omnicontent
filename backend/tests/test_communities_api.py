"""
Tests for community management API endpoints.

Endpoints tested:
- GET /api/communities
- POST /api/communities
- GET /api/communities/{community_id}
- PUT /api/communities/{community_id}
- DELETE /api/communities/{community_id}
- POST /api/communities/{community_id}/users
- DELETE /api/communities/{community_id}/users/{user_id}
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.community import Community


class TestListCommunities:
    """Tests for GET /api/communities"""

    def test_list_communities_success(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Test listing communities for authenticated user."""
        response = client.get("/api/communities", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert len(data["items"]) >= 1
        assert data["items"][0]["name"] == "Test Community"

    def test_list_communities_no_auth(self, client: TestClient):
        """Test listing communities fails without authentication."""
        response = client.get("/api/communities")
        assert response.status_code == 401

    def test_list_communities_pagination(
        self,
        client: TestClient,
        db_session: Session,
        test_user: User,
        auth_headers: dict,
    ):
        """Test communities list pagination."""
        # Create multiple communities for the user
        for i in range(5):
            community = Community(
                name=f"Community {i}",
                slug=f"community-{i}",
                description=f"Description {i}",
            )
            test_user.communities.append(community)
        db_session.commit()

        # Test first page
        response = client.get(
            "/api/communities?page=1&page_size=3", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["page"] == 1
        assert data["page_size"] == 3
        assert data["total"] >= 5

    def test_list_communities_isolation(
        self,
        client: TestClient,
        test_user: User,
        test_another_user: User,
        auth_headers: dict,
    ):
        """Test users only see their own communities."""
        response = client.get("/api/communities", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        # Should only see test_user's communities, not another user's
        community_names = [c["name"] for c in data["items"]]
        assert "Test Community" in community_names
        assert "Another Community" not in community_names


class TestCreateCommunity:
    """Tests for POST /api/communities"""

    def test_create_community_success(
        self, client: TestClient, superuser_auth_headers: dict
    ):
        """Test creating a new community as superuser."""
        response = client.post(
            "/api/communities",
            headers=superuser_auth_headers,
            json={
                "name": "New Community",
                "slug": "new-community",
                "description": "A brand new community",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Community"
        assert data["slug"] == "new-community"
        assert data["description"] == "A brand new community"
        assert data["is_active"] is True

    def test_create_community_forbidden_for_regular_user(
        self, client: TestClient, auth_headers: dict
    ):
        """Test regular users cannot create communities."""
        response = client.post(
            "/api/communities",
            headers=auth_headers,
            json={
                "name": "Forbidden Community",
                "slug": "forbidden",
                "description": "This should fail",
            },
        )
        assert response.status_code == 403

    def test_create_community_duplicate_slug(
        self,
        client: TestClient,
        test_community: Community,
        superuser_auth_headers: dict,
    ):
        """Test creating community with duplicate slug fails."""
        response = client.post(
            "/api/communities",
            headers=superuser_auth_headers,
            json={
                "name": "Different Name",
                "slug": "test-community",  # Already exists
                "description": "Different description",
            },
        )
        assert response.status_code == 400
        assert "slug" in response.json()["detail"].lower()

    def test_create_community_no_auth(self, client: TestClient):
        """Test creating community fails without authentication."""
        response = client.post(
            "/api/communities",
            json={
                "name": "No Auth Community",
                "slug": "no-auth",
                "description": "Should fail",
            },
        )
        assert response.status_code == 401


class TestGetCommunity:
    """Tests for GET /api/communities/{community_id}"""

    def test_get_community_success(
        self,
        client: TestClient,
        test_community: Community,
        auth_headers: dict,
    ):
        """Test getting community details."""
        response = client.get(
            f"/api/communities/{test_community.id}", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Community"
        assert data["slug"] == "test-community"
        assert "members" in data
        assert len(data["members"]) >= 1

    def test_get_community_not_found(
        self, client: TestClient, auth_headers: dict
    ):
        """Test getting non-existent community returns 404."""
        response = client.get("/api/communities/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_get_community_no_access(
        self,
        client: TestClient,
        test_another_community: Community,
        auth_headers: dict,
    ):
        """Test getting community user doesn't have access to."""
        response = client.get(
            f"/api/communities/{test_another_community.id}", headers=auth_headers
        )
        assert response.status_code == 403

    def test_get_community_no_auth(
        self, client: TestClient, test_community: Community
    ):
        """Test getting community fails without authentication."""
        response = client.get(f"/api/communities/{test_community.id}")
        assert response.status_code == 401


class TestUpdateCommunity:
    """Tests for PUT /api/communities/{community_id}"""

    def test_update_community_success(
        self,
        client: TestClient,
        test_community: Community,
        auth_headers: dict,
    ):
        """Test updating community information."""
        response = client.put(
            f"/api/communities/{test_community.id}",
            headers=auth_headers,
            json={
                "name": "Updated Community",
                "description": "Updated description",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Community"
        assert data["description"] == "Updated description"
        assert data["slug"] == "test-community"  # Slug should not change

    def test_update_community_no_access(
        self,
        client: TestClient,
        test_another_community: Community,
        auth_headers: dict,
    ):
        """Test updating community user doesn't have access to."""
        response = client.put(
            f"/api/communities/{test_another_community.id}",
            headers=auth_headers,
            json={"name": "Hacked"},
        )
        assert response.status_code == 403

    def test_update_community_not_found(
        self, client: TestClient, auth_headers: dict
    ):
        """Test updating non-existent community returns 404."""
        response = client.put(
            "/api/communities/99999",
            headers=auth_headers,
            json={"name": "Not Found"},
        )
        assert response.status_code == 404


class TestDeleteCommunity:
    """Tests for DELETE /api/communities/{community_id}"""

    def test_delete_community_success(
        self,
        client: TestClient,
        db_session: Session,
        test_superuser: User,
        superuser_auth_headers: dict,
    ):
        """Test deleting community as superuser."""
        # Create a community to delete
        community = Community(
            name="To Delete",
            slug="to-delete",
            description="Will be deleted",
        )
        test_superuser.communities.append(community)
        db_session.add(community)
        db_session.commit()
        community_id = community.id

        response = client.delete(
            f"/api/communities/{community_id}",
            headers=superuser_auth_headers,
        )
        assert response.status_code == 204

        # Verify community is deleted
        deleted = db_session.get(Community, community_id)
        assert deleted is None

    def test_delete_community_forbidden_for_regular_user(
        self,
        client: TestClient,
        test_community: Community,
        auth_headers: dict,
    ):
        """Test regular users cannot delete communities."""
        response = client.delete(
            f"/api/communities/{test_community.id}",
            headers=auth_headers,
        )
        assert response.status_code == 403

    def test_delete_community_not_found(
        self, client: TestClient, superuser_auth_headers: dict
    ):
        """Test deleting non-existent community returns 404."""
        response = client.delete(
            "/api/communities/99999",
            headers=superuser_auth_headers,
        )
        assert response.status_code == 404


class TestAddUserToCommunity:
    """Tests for POST /api/communities/{community_id}/users"""

    def test_add_user_success(
        self,
        client: TestClient,
        db_session: Session,
        test_community: Community,
        superuser_auth_headers: dict,
    ):
        """Test adding user to community as superuser."""
        # Create a user not in the community
        from app.core.security import get_password_hash

        new_user = User(
            username="newmember",
            email="newmember@example.com",
            hashed_password=get_password_hash("pass123"),
            is_active=True,
        )
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        response = client.post(
            f"/api/communities/{test_community.id}/users",
            headers=superuser_auth_headers,
            json={"user_id": new_user.id},
        )
        assert response.status_code == 200
        data = response.json()
        member_ids = [m["id"] for m in data["members"]]
        assert new_user.id in member_ids

    def test_add_user_forbidden_for_regular_user(
        self,
        client: TestClient,
        test_community: Community,
        test_another_user: User,
        auth_headers: dict,
    ):
        """Test regular users cannot add members to communities."""
        response = client.post(
            f"/api/communities/{test_community.id}/users",
            headers=auth_headers,
            json={"user_id": test_another_user.id},
        )
        assert response.status_code == 403

    def test_add_user_already_member(
        self,
        client: TestClient,
        test_community: Community,
        test_user: User,
        superuser_auth_headers: dict,
    ):
        """Test adding user who is already a member."""
        response = client.post(
            f"/api/communities/{test_community.id}/users",
            headers=superuser_auth_headers,
            json={"user_id": test_user.id},
        )
        assert response.status_code == 400
        assert "already a member" in response.json()["detail"].lower()

    def test_add_nonexistent_user(
        self,
        client: TestClient,
        test_community: Community,
        superuser_auth_headers: dict,
    ):
        """Test adding non-existent user fails."""
        response = client.post(
            f"/api/communities/{test_community.id}/users",
            headers=superuser_auth_headers,
            json={"user_id": 99999},
        )
        assert response.status_code == 404


class TestRemoveUserFromCommunity:
    """Tests for DELETE /api/communities/{community_id}/users/{user_id}"""

    def test_remove_user_success(
        self,
        client: TestClient,
        db_session: Session,
        test_community: Community,
        superuser_auth_headers: dict,
    ):
        """Test removing user from community as superuser."""
        # Create and add a user to remove
        from app.core.security import get_password_hash

        user_to_remove = User(
            username="toremove",
            email="toremove@example.com",
            hashed_password=get_password_hash("pass123"),
            is_active=True,
        )
        user_to_remove.communities.append(test_community)
        db_session.add(user_to_remove)
        db_session.commit()
        user_id = user_to_remove.id

        response = client.delete(
            f"/api/communities/{test_community.id}/users/{user_id}",
            headers=superuser_auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        member_ids = [m["id"] for m in data["members"]]
        assert user_id not in member_ids

    def test_remove_user_forbidden_for_regular_user(
        self,
        client: TestClient,
        test_community: Community,
        test_user: User,
        auth_headers: dict,
    ):
        """Test regular users cannot remove members from communities."""
        response = client.delete(
            f"/api/communities/{test_community.id}/users/{test_user.id}",
            headers=auth_headers,
        )
        assert response.status_code == 403

    def test_remove_user_not_member(
        self,
        client: TestClient,
        test_community: Community,
        test_another_user: User,
        superuser_auth_headers: dict,
    ):
        """Test removing user who is not a member."""
        response = client.delete(
            f"/api/communities/{test_community.id}/users/{test_another_user.id}",
            headers=superuser_auth_headers,
        )
        assert response.status_code == 404

    def test_remove_nonexistent_user(
        self,
        client: TestClient,
        test_community: Community,
        superuser_auth_headers: dict,
    ):
        """Test removing non-existent user fails."""
        response = client.delete(
            f"/api/communities/{test_community.id}/users/99999",
            headers=superuser_auth_headers,
        )
        assert response.status_code == 404
