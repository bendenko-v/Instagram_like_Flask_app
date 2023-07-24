# Flask Instagram-like App

This is a simple Flask application that serves as an Instagram-like platform, focusing on practice using Jinja templates and handling JSON data. The app allows users to view and interact with posts, including adding posts to favorites, leaving comments, and performing searches based on post descriptions and hashtags.

![Main page](https://habrastorage.org/webt/0s/3t/zw/0s3tzwevjh8r8tv2dmo6hnsrcqu.jpeg)

## Usage

1. Install dependencies `pip install -r requirements.txt`
2. To run the Flask app, use the following command: `python app.py`
3. This will start the development server, and you can access the app by visiting http://localhost:5000 in your web browser.

## App features

The main functionality of the app includes:
- **View All Posts**: On the homepage, all posts are displayed with their titles, descriptions, and bookmarks flag.
- **View Individual Post**: User can click on a post to view it individually, including its full description and comments.
- **Add to Favorites**: User can add posts to their favorites by clicking on the "Add to Favorites" button.
- **Leave Comments**: User can leave comments on individual posts.
- **Search by Text**: The app provides a search functionality to find posts based on text in their descriptions.
- **Search by Hashtag**: Users can search for posts using hashtags mentioned in the descriptions.

## Note
This application is created for educational purposes to practice working with Flask, Jinja templates, and JSON data. It does not include user registration or authentication, and it is not intended for production use.