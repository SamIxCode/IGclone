# Social Media Django App
A social media application developed using Django that allows users to sign up, log in, post updates, like and comment on other user's updates and follow other users.

## Features
- User authentication: sign up, log in, log out
- User profile management: edit profile and change profile picture
- Post management: create and view updates
- Like and comment management
- Follow/unfollow management
- User suggestions based on who they follow
## Technical details
- Django's built-in authentication views and decorators are used for user authentication and access control.
- Django models are used to represent the User, Profile, Post, LikePost and FollowerCount data.
- Django forms are used for creating new users and editing profiles.
- Django templates are used for rendering HTML pages.
## Getting started
- Clone the repository and install the required packages using `pip install -r requirements.txt`
- Run migrations to set up the database using `python manage.py migrate`.
- Run the local server using `python manage.py runserver`.
- Access the application on your browser at http://localhost:8000
### Contributing

If you are interested in contributing to the development of this project, feel free to submit a pull request.
