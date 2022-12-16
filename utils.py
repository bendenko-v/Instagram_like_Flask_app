from __future__ import annotations

import re
import json
from json import JSONDecodeError


def load_data(path: str) -> list[dict] | None:
    """
    Load data from json-file
    Args:
        path: path to json-file
    Returns:
        list of dicts with data or None if exceptions
    """
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None
    except JSONDecodeError:
        return None


def save_data(path: str, data: list[dict]) -> None:
    """
    Save data to json-file
    Args:
        path: path to json-file
        data: list of dicts with data to write
    """
    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_all_posts(path: str) -> list | None:
    """
    Load all posts
    Returns:
        list of dicts with data or None
    """
    all_posts = load_data(path)
    return all_posts


def search_posts(search_text: str, path: str) -> list[dict] | []:
    """
    Search text in the posts
    Args:
        search_text: search query
        path: path to posts.json
    Returns:
        list of dicts with user's posts or empty list
    """
    all_posts = load_data(path)
    found_posts = []
    try:
        for post in all_posts:
            if search_text.lower() in post['content'].lower():
                found_posts.append(post)
        return found_posts
    except TypeError:
        return []


def get_posts_by_user(user_name: str, path: str) -> list[dict] | []:
    """
    Load user posts
    Args:
        user_name: username to download posts
        path: path to posts.json
    Returns:
        list of dicts with user's posts or empty list
    """
    all_posts = load_data(path)
    user_posts = []
    try:
        for post in all_posts:
            if post['author'].lower() == user_name.lower():
                user_posts.append(post)
        return user_posts
    except TypeError:
        return []


def get_post_by_pk(pk: int, path: str) -> dict | None:
    """
    Load the post by primary key
    Args:
        pk: primary key of the post
        path: path to posts.json
    Returns:
        dict with post's data
    """
    all_posts = load_data(path)
    for post in all_posts:
        if post['pk'] == pk:
            post = check_hashtag(post)
            return post
    return None


def check_hashtag(post):
    if '#' in post['content']:
        for match in re.findall(r'#\w+[\s\w]', post['content']):
            post['content'] = post['content'].replace(match,
                                                      f'<a class="link" href="/tag/{match.strip()[1:]}">{match}</a>')
    return post


def get_posts_by_tag(tag: str, path: str) -> list[dict] | []:
    """
    Load the posts that contain #tag
    Args:
        tag: tag to search
        path: path to posts.json
    Returns:
        dict with post's data
    """
    all_posts = load_data(path)
    found_posts = []
    try:
        for post in all_posts:
            if '#' + tag in post['content']:
                post = check_hashtag(post)
                found_posts.append(post)
        return found_posts
    except TypeError:
        return []


def add_views(pk: int, path: str) -> None:
    """
    Increase views by +1
    Args:
        pk: primary key of the post
        path: path to posts.json
    Returns:

    """
    all_posts = load_data(path)
    for post in all_posts:
        if post['pk'] == pk:
            post['views_count'] += 1
    save_data(path, all_posts)


def get_comments_by_post_id(post_id: int, new_comment: str | None, path: str) -> list[dict] | []:
    """
    Load comments for the post
    Args:
        new_comment: if new_comment exists it will add to all comments
        post_id: primary key of the post
        path: path to comments.json
    Returns:
        list of dicts with comments or empty list
    """
    all_comments = load_data(path)
    if not all_comments:
        return []
    if new_comment:
        all_comments.append(
            {
                "post_id": post_id,
                "commenter_name": "Vadim",
                "content": new_comment,
                "pk": len(all_comments) + 1
            }
        )
        save_data(path, all_comments)
    post_comments = []
    for comment in all_comments:
        if comment['post_id'] == post_id:
            post_comments.append(comment)
    return post_comments


def add__bookmark(pk: int, path: str) -> None:
    """
    Add bookmark to post
    Args:
        pk: primary key of the post
        path: path to bookmarks.json
    """
    bookmarks = load_data(path)
    for mark in bookmarks:
        if pk == mark['pk']:
            mark['bookmark'] = True
    save_data(path, bookmarks)


def remove__bookmark(pk: int, path: str) -> None:
    """
    Remove bookmark from post
    Args:
        pk: primary key of the post
        path: path to bookmarks.json
    """
    bookmarks = load_data(path)
    for mark in bookmarks:
        if pk == mark['pk']:
            mark['bookmark'] = False
    save_data(path, bookmarks)


def load_bookmarks(path: str) -> tuple[int, list[dict]] | None:
    """
    Load bookmarks data
    Args:
        path: path to bookmarks.json
    Returns:
        tuple with quantity of added bookmarks and bookmarks data or None
    """
    bookmarks = load_data(path)
    if not bookmarks:
        return None
    count_bookmarks = 0
    for mark in bookmarks:
        if mark['bookmark']:
            count_bookmarks += 1
    return count_bookmarks, bookmarks


def load_bookmarks_posts(path_to_posts: str, path_to_bookmarks: str) -> list[dict] | None:
    """
    Load data of all posts with added bookmarks
    Args:
        path_to_posts: path to posts.json
        path_to_bookmarks: path to bookmarks.json
    Returns:
        list of dicts with data or None
    """
    bookmarks_posts = []
    all_posts = load_data(path_to_posts)
    bookmarks = load_data(path_to_bookmarks)
    if not all_posts or not bookmarks:
        return None
    for m in range(len(bookmarks)):
        if bookmarks[m]['bookmark']:
            bookmarks_posts.append(all_posts[m])
    return bookmarks_posts
