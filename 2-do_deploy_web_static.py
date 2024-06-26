#!/usr/bin/python3
"""Fabric script to deploy a .tgz archive to web servers"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

# Replace 'xx-web-01', 'xx-web-02' with your server IPs
env.hosts = ['107.22.142.174', '3.85.1.94']


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Extract the archive to
        # /data/web_static/releases/<archive_filename without extension>/
        archive_filename = archive_path.split('/')[-1]
        folder_name = archive_filename.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_filename, folder_name))

        # Remove the uploaded archive from the server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the extracted folder to the releases folder
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(folder_name, folder_name))

        # Remove the now empty web_static folder
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(folder_name))

        # Update the symbolic link to the new version
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(folder_name))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Error deploying archive:", e)
        return False


if __name__ == "__main__":
    # Usage: fab -f 2-do_deploy_web_static.py do_deploy:archive_path=versions
    # /web_static_20170315003959.tgz -i my_ssh_private_key -u ubuntu
    pass
