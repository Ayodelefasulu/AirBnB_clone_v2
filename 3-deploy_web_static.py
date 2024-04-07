#!/usr/bin/python3
"""Fabric script to deploy a .tgz archive to web servers"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

# Replace 'xx-web-01', 'xx-web-02' with your server IPs
env.hosts = ['xx-web-01', 'xx-web-02']


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/<archive_filename
        # without extension>/
        archive_filename = archive_path.split('/')[-1]
        folder_name = archive_filename.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_filename, folder_name))

        # Remove the uploaded archive from the server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the extracted folder to the releases folder
        run('mv /data/web_static/releases/{}/web_static/*'
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


def do_pack():
    """Generates a .tgz archive from the web_static folder"""
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


def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    # Example usage: fab -f 3-deploy_web_static.py deploy -i
    # my_ssh_private_key -u ubuntu
    pass
