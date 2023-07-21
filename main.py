# Import required libraries
import subprocess
import os
import sys

# Define the Docker Compose YAML template for the LEMP stack (Linux, Nginx, MySQL, PHP)
LEMP_TEMPLATE = """
version: '3'
services:
  wordpress:
    image: wordpress:latest
    ports:
      - "80:80"
    environment:
      - WORDPRESS_DB_HOST=db
      - WORDPRESS_DB_NAME=wordpress
      - WORDPRESS_DB_USER=root
      - WORDPRESS_DB_PASSWORD=password
    volumes:
      - ./wordpress:/var/www/html
  db:
    image: mariadb
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=wordpress
    volumes:
      - ./db:/var/lib/mysql
"""

# Function to check if Docker is installed
def is_docker_installed():
    try:
        # Check if Docker is installed by running the "docker --version" command
        subprocess.check_output(['docker', '--version'], stderr=subprocess.STDOUT, universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to check if Docker Compose is installed
def is_docker_compose_installed():
    try:
        # Check if Docker Compose is installed by running the "docker-compose --version" command
        subprocess.check_output(['docker-compose', '--version'], stderr=subprocess.STDOUT, universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to install Docker using apt package manager
def install_docker():
    try:
        subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'docker'])
        return True
    except subprocess.CalledProcessError:
        return False

# Function to install Docker Compose
def install_docker_compose():
    try:
        subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'docker-compose'])
        return True
    except subprocess.CalledProcessError:
        return False

# Function to create a WordPress site using Docker Compose
def create_wordpress_site(site_name):
    if os.path.exists(site_name):
        print(f"The directory '{site_name}' already exists. Please choose a different name.")
        sys.exit(1)

    # Create the directory for the site and move to that directory
    os.makedirs(site_name)
    os.chdir(site_name)

    with open("docker-compose.yml", "w") as f:
        f.write(LEMP_TEMPLATE)

    # Create a Docker network with the site name
    subprocess.call(['docker', 'network', 'create', site_name])

    # Start the containers using Docker Compose
    subprocess.call(['docker-compose', 'up', '-d'])

    # Add an entry to /etc/hosts to map the site_name to localhost
    with open('/etc/hosts', 'a') as f:
        f.write(f"127.0.0.1 {site_name}\n")

# Function to enable a WordPress site using Docker Compose
def enable_site(site_name):
    if not os.path.exists(site_name):
        print(f"The site '{site_name}' does not exist and thus can't be enabled. Create it first.")
        sys.exit(1)
    
    # Start the containers for the site using Docker Compose
    subprocess.call(['docker-compose', '-f', f'{site_name}/docker-compose.yml', 'up', '-d'])
    print(f"The site '{site_name}' has been enabled.")

# Function to disable a WordPress site using Docker Compose
def disable_site(site_name):
    if not os.path.exists(site_name):
        print(f"The site '{site_name}' does not exist and thus can't be disabled. Create it first.")
        sys.exit(1)
    
    # Stop and remove the containers for the site using Docker Compose
    subprocess.call(['docker-compose', '-f', f'{site_name}/docker-compose.yml', 'down'])
    print(f"The site '{site_name}' has been disabled.")

# Function to delete a WordPress site created with Docker Compose
def delete_wordpress_site(site_name):
    if not os.path.exists(site_name):
        print(f"The site '{site_name}' does not exist.")
        sys.exit(1)

    # Change the working directory to the site directory
    os.chdir(site_name)

    # Stop and remove the containers for the site using Docker Compose
    subprocess.run(["docker-compose", "down", "-v"])

    # Move back to the parent directory and remove the site directory
    os.chdir("..")
    subprocess.run(["rm", "-rf", site_name])

    # Remove the site name entry from /etc/hosts
    subprocess.run(["sudo", "sed", "-i", f"/{site_name}/d", "/etc/hosts"])
    
    print(f"The site '{site_name}' has been deleted.")

def main():
    
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <command> <site_name>")
        return
    
    # Extract the command and site name from command-line arguments
    command = sys.argv[1]
    site_name = sys.argv[2]

    # Perform the specified command based on user input
    if command == "create":
        if not is_docker_installed():
            print("Docker is not installed. Installing Docker...")
            if install_docker():
                print("Docker installed successfully.")
            else:
                print("Failed to install Docker.")
        else:
            print("Docker is already installed.")

        if not is_docker_compose_installed():
            print("Docker Compose is not installed. Installing Docker Compose...")
            if install_docker_compose():
                print("Docker Compose installed successfully.")
            else:
                print("Failed to install Docker Compose.")
        else:
            print("Docker Compose is already installed.")
    
        create_wordpress_site(site_name)

        print(f"Please open http://{site_name} in your browser.")

    elif command == "enable":
        enable_site(site_name)
    
    elif command == "disable":
        disable_site(site_name)

    elif command == 'delete':
        delete_wordpress_site(site_name)

    else:
        print("Invalid command")

if __name__ == '__main__':
    main()