import pytest

from utils import *
from config import POSTS, COMMENTS, BOOKMARKS


@pytest.mark.parametrize('path', (POSTS, COMMENTS, BOOKMARKS))
def test_load_json(path):
    json_data = load_data(path)
    assert type(json_data) == list, f'Ошибка загрузки данных из JSON-файла {path}!'
    for d in json_data:
        assert type(d) == dict, f'Ошибка! Внутри JSON-файла {path} нет словарей!'


def test_load_json_if_not_found():
    assert load_data('file_not_found.json') is None


def test_save_json():
    json_example = [
        {
            "pk": 1,
            "author": "Name",
            "avatar": "https://i.pravatar.cc/94?img=11",
            "image": "some_image.jpg",
            "content": "some text",
            "date": "16-11-2022",
            "views_count": 10,
            "likes_count": 3
        }
    ]
    save_data('tests/test_file.json', json_example)
    test_load_json('tests/test_file.json')


def test_get_all_posts():
    posts_data = get_all_posts(POSTS)
    params = ('pk', 'author', 'avatar', 'image', 'content', 'date', 'views_count', 'likes_count')
    assert type(posts_data) == list, 'Данные постов не загружены!'
    for post in posts_data:
        for p in params:
            assert p in post, f'В данных поста отсутствует параметр {p}'


def test_search_text():
    assert len(search_posts('1212131', POSTS)) == 0, 'Некорректный ответ при поиске текста "1212131"'
    assert len(search_posts('lake', POSTS)) > 0, 'Не найдены посты при поиске текста "lake"'


@pytest.mark.parametrize('user', ('Sasha', 'Boris', 'Vika'))
def test_posts_by_user(user):
    assert len(get_posts_by_user(user, POSTS)) > 0, f'Не найдены посты автора - {user}'


def test_posts_by_not_user():
    assert len(get_posts_by_user('Миша', POSTS)) == 0, 'Найдены посты несуществующего автора Миши'


@pytest.mark.parametrize('pk', [*range(1, 7)])
def test_posts_by_pk(pk):
    assert len(get_post_by_pk(pk, POSTS)) == 8, f'Неверные данные поста с pk = {pk}'


@pytest.mark.parametrize('tag', ('lake', 'town', 'happiness', 'mountains'))
def test_get_posts_by_tag(tag):
    assert len(get_posts_by_tag(tag, POSTS)) > 0, f'Не найдены посты с тегом #{tag}'
