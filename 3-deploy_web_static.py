#!/usr/bin/python3
""" Used to deploy with fabric  """
from fabric import task, Connection, Config, env
from datetime import datetime
import os

# Define Fabric environment variables
env.hosts = ['107.22.142.174', '3.85.1.94']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/school'

@task
def do_pack(c):
    """Generates a .tgz archive from the web_static folder"""
    try:
        # Create the versions directory if it doesn't exist
        c.local("mkdir -p versions")

        # Get the current date and time
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Create the archive filename with the timestamp
        archive_name = "versions/web_static_{}.tgz".format(timestamp)
        # Create the .tgz archive from the web_static folder
        c.local("tar -cvzf {} web_static".format(archive_name))

        # Return the archive path if successful
        return archive_name
    except Exception as e:
        print("Error packing web_static:", e)
        return None

@task
def do_deploy(c, archive_path):
    """Deploys an archive to the web servers"""
    if not os.path.exists(archive_path):
        print(f"Archive {archive_path} not found. Deployment aborted.")
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        c.put(archive_path, '/tmp/')

        # Uncompress the archive to the folder
        folder_name = os.path.splitext(os.path.basename(archive_path))[0]
        c.run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        c.run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(os.path.basename(archive_path), folder_name))

        # Remove the archive from the web server
        c.run('rm /tmp/{}'.format(os.path.basename(archive_path)))

        # Move the contents to the correct location
        c.run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(folder_name, folder_name))
        c.run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))

        # Update the symbolic link
        c.run('rm -rf /data/web_static/current')
        c.run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Error deploying:", e)
        return False

@task
def deploy(c):
    """Deploys the web_static project"""
    # Call do_pack and store the archive path
    archive_path = do_pack(c)
    if not archive_path:
        print("No archive created. Deployment aborted.")
        return False

    # Call do_deploy with the archive path
    return do_deploy(c, archive_path)

