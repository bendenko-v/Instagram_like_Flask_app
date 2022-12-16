import pytest

from app import app


def test_get_index():
    response = app.test_client().get('/')
    assert response.status_code == 200


def test_post_index():
    response = app.test_client().post('/')
    assert response.status_code == 405


@pytest.mark.parametrize("s", ('lake', 'monte', 'happiness', "", "1212356sdfsd"))
def test_search(s):
    params = {"s": s}
    response = app.test_client().get('/', query_string=params)
    assert response.status_code == 200


@pytest.mark.parametrize('name', ('Boris', 'Sasha', 'Vika'))
def test_user_page(name):
    response = app.test_client().get(f'/user/{name}')
    assert response.status_code == 200


def test_false_user_page():
    response = app.test_client().get(f'/user/falsename')
    assert response.status_code == 404


@pytest.mark.parametrize('tag', ('lake', 'town', 'happiness', 'mountains'))
def test_search_by_tag(tag):
    response = app.test_client().get(f'/tag/{tag}')
    assert response.status_code == 200


def test_search_by_false_tag():
    response = app.test_client().get(f'/tag/falsetag')
    assert response.status_code == 404


@pytest.mark.parametrize('pk', [*range(1, 7)])
def test_post_page(pk):
    response = app.test_client().get(f'/posts/{pk}')
    assert response.status_code == 200


def test_false_post_page():
    response = app.test_client().get(f'/posts/falsepk')
    assert response.status_code == 404


def test_add_comment():
    """ During the test adds comment to comments.json """
    data = {'new_comment': 'Test: Adding comment to post 1'}
    response = app.test_client().post(f'/posts/1/new_comment', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test: Adding comment to post 1" in response.data


def test_favorites():
    response = app.test_client().get('/bookmarks/')
    assert response.status_code == 200


def test_add_remove_bookmark():
    response = app.test_client().get('/bookmarks/add/1', follow_redirects=True)
    assert response.status_code == 200
    response = app.test_client().get('/bookmarks/remove/1', follow_redirects=True)
    assert response.status_code == 200


def test_api_posts():
    response = app.test_client().get('/api/posts/')
    assert response.status_code == 200
    assert len(response.json) == 6


@pytest.mark.parametrize('pk', [*range(1, 7)])
def test_api_post(pk):
    response = app.test_client().get(f'/api/posts/{pk}')
    params = ('pk', 'author', 'avatar', 'image', 'content', 'date', 'views_count', 'likes_count')
    assert response.status_code == 200
    assert len(response.json) == 8
    for param in params:
        assert param in response.json
