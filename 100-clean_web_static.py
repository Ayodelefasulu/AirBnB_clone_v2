#!/usr/bin/python3
"""Fabric script to clean up outdated archives"""

from fabric.api import env, local, run
from datetime import datetime
from os.path import exists

# Replace 'xx-web-01', 'xx-web-02' with your server IPs
env.hosts = ['107.22.142.174', '3.85.1.94']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/school'


def do_clean(number=0):
    """Deletes out-of-date archives"""
    try:
        number = int(number)
        if number < 0:
            number = 0
        elif number == 0:
            number = 1

        # Get a list of all files in versions folder sorted by modification time
        files = local('ls -1t versions', capture=True).split('\n')

        # Remove the number of archives to keep, starting from the second one
        for file in files[number:]:
            local('rm versions/{}'.format(file))

        # Get a list of all files in /data/web_static/releases folder on the servers
        releases_files = run('ls -1t /data/web_static/releases').split('\n')

        # Remove the number of archives to keep, starting from the second one
        for file in releases_files[number:]:
            run('rm -rf /data/web_static/releases/{}'.format(file))

        print("Cleaned up archives successfully!")
        return True
    except Exception as e:
        print("Error cleaning up archives:", e)
        return False


if __name__ == "__main__":
    do_clean()
