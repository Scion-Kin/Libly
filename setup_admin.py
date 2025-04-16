#!/usr/bin/python3
# This will be executed by the server set up script to make the admin user

# must executed as main

import os
import sys
from models.user import User

def create_admin_user():
    """ Create an admin user """
    admin_user = User()
    admin_user.email = os.getenv("ADMIN_EMAIL")
    admin_user.password = os.getenv("ADMIN_PASSWORD")
    admin_user.user_type = "librarian"
    admin_user.first_name = "Libly"
    admin_user.last_name = "Admin"
    admin_user.onboarded = True
    admin_user.confirmed = True
    admin_user.pic = 'imageedit_6_4239771167.jpg'
    admin_user.save()

if __name__ == "__main__":
    if os.getenv("ADMIN_EMAIL") is None or os.getenv("ADMIN_PASSWORD") is None:
        print("Please set the ADMIN_EMAIL and ADMIN_PASSWORD environment variables.")
        sys.stdout.write()
        sys.exit(1)
    create_admin_user()
