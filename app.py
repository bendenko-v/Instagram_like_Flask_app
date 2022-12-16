import logging
from flask import Flask, render_template, abort, request, redirect, jsonify, send_from_directory

from utils import *
from config import *

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler(filename=os.path.join('logs', 'api.log'),
                                                  encoding='utf-8',
                                                  mode='a+')
                              ]
                    )


@app.route('/')
def index():
    """ View main page or Search results page if we get "s" parameter """
    s = request.args.get('s')
    is_search = False

    if s:
        posts = search_posts(s, POSTS)
        is_search = True
    else:
        posts = get_all_posts(POSTS)

    if not posts and not is_search:
        abort(404)

    count_marks, bookmarks = load_bookmarks(BOOKMARKS)

    title = '[...gram]'

    return render_template('index.html',
                           title=title,
                           posts=posts,
                           is_search=is_search,
                           count_marks=count_marks,
                           bookmarks=bookmarks
                           )


@app.route('/user/<user_name>')
def user_page(user_name):
    """ View page with 'user_name' posts """
    user_posts = get_posts_by_user(user_name, POSTS)
    count_marks, bookmarks = load_bookmarks(BOOKMARKS)

    if not user_posts:
        abort(404)

    title = user_name + "'s posts"

    return render_template('index.html',
                           title=title,
                           posts=user_posts,
                           count_marks=count_marks,
                           bookmarks=bookmarks
                           )


@app.route('/tag/<tag>')
def search_by_tag(tag):
    """ View page with posts by hashtag """
    posts = get_posts_by_tag(tag, POSTS)
    count_marks, bookmarks = load_bookmarks(BOOKMARKS)

    if not posts:
        abort(404)

    title = f'Posts with #{tag}'

    return render_template('index.html',
                           title=title,
                           posts=posts,
                           count_marks=count_marks,
                           bookmarks=bookmarks
                           )


@app.route('/posts/<int:pk>')
def post_page(pk):
    """ View page with post by 'pk' identifier """
    add_views(pk, POSTS)  # increase views +1
    post = get_post_by_pk(pk, POSTS)

    if not post:
        abort(404)

    comments = get_comments_by_post_id(pk, None, COMMENTS)
    _, bookmarks = load_bookmarks(BOOKMARKS)

    title = f"Post #{pk}"

    return render_template('post.html',
                           title=title,
                           post=post,
                           comments=comments,
                           bookmarks=bookmarks
                           )


@app.route('/posts/<int:pk>/new_comment', methods=['POST'])
def add_comment(pk):
    """ Add comment to 'pk' post by POST method """
    post = get_post_by_pk(pk, POSTS)
    if request.method == 'POST':
        new_comment = request.values.get('new_comment')
    else:
        new_comment = None

    comments = get_comments_by_post_id(pk, new_comment, COMMENTS)
    _, bookmarks = load_bookmarks(BOOKMARKS)

    title = f"Post #{pk}"

    return render_template('post.html',
                           title=title,
                           post=post,
                           comments=comments,
                           bookmarks=bookmarks
                           )


@app.route('/bookmarks/')
def favorites():
    bookmarks_posts = load_bookmarks_posts(POSTS, BOOKMARKS)
    count_marks, bookmarks = load_bookmarks(BOOKMARKS)

    title = "My bookmarks"

    return render_template('index.html',
                           title=title,
                           posts=bookmarks_posts,
                           count_marks=count_marks,
                           bookmarks=bookmarks
                           )


@app.route('/bookmarks/add/<int:pk>')
def add_bookmark(pk):
    add__bookmark(pk, BOOKMARKS)
    return redirect('/', code=302)


@app.route('/bookmarks/remove/<int:pk>')
def remove_bookmark(pk):
    remove__bookmark(pk, BOOKMARKS)
    return redirect('/', code=302)


@app.route('/api/posts/', methods=['GET'])
def api_posts():
    logging.info('Request /api/posts')
    return jsonify(get_all_posts(POSTS))


@app.route('/api/posts/<int:pk>', methods=['GET'])
def api_post_by_pk(pk):
    logging.info(f'Request /api/posts/{pk}')
    return jsonify(get_post_by_pk(pk, POSTS))


@app.route('/images/<filename>')
def get_image_link(filename):
    return send_from_directory(POSTS_IMAGES, filename)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', title='404 Not found'), 404


@app.errorhandler(500)
def render_server_error(error):
    return render_template('500.html', title='500 Internal Server Error'), 500


if __name__ == '__main__':
    app.run()
