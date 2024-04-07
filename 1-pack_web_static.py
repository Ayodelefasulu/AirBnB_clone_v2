#!/usr/bin/env python3
"""
Fabric script to generate a .tgz archive from the web_static folder
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the web_static folder

    Returns:
        str: Archive path if successful, None otherwise
    """
    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")

        # Get the current date and time
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Create the archive filename with the timestamp
        archive_name = "versions/web_static_{}.tgz".format(timestamp)

        # Create the .tgz archive from the web_static folder
        local("tar -cvzf {} web_static".format(archive_name))

        # Return the archive path if successful
        return archive_name
    except Exception as e:
        print("Error packing web_static:", e)
        return None


if __name__ == "__main__":
    do_pack()
