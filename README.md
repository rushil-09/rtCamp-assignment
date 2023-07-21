### rtCamp-assignment
This assignment is part of the selection process for DevOps Engineer at rtCamp.

# WordPress Site Management with Docker Compose
This Python script allows you to manage WordPress sites using Docker Compose easily. This script allows you to create, enable, disable, and delete WordPress sites running in Docker containers.

## Usage
To use the script, follow these steps:
1. Ensure that Python 3 is installed on your system.
2. Download or clone this repository to your local machine.
3. Open a terminal and navigate to the directory containing the script (main.py).
4. Required template of the command line is as follows : 
```bash
   python main.py <command> <site_name>
```
  - **command** can be one of the following:
    - **'create'**: Create a new WordPress site running in Docker containers.
    - **'enable'**: Start the containers for an existing WordPress site.
    - **'disable'**: Stop the containers for an existing WordPress site.
    - **'delete'**: Delete an existing WordPress site.

  - **'<site_name>'** is the name of the WordPress site you want to manage. This will be used as the directory name for the site.

**5. Examples:**

  - Create a new WordPress site named "myblog.com".

```bash
   sudo python3 main.py create myblog.com
```

This command creates a new WordPress site using the latest WordPress version and will install Docker and Docker Compose if they are not already installed, create the necessary containers, set up the WordPress site, and add an entry to /etc/hosts to access the site.

  - Enable an existing WordPress site named "myblog.com":

```bash
   sudo python3 main.py enable myblog.com
```
This command will start the containers for the specified site.

   - Disable an existing WordPress site named "myblog.com":

```bash
   sudo python3 main.py disable myblog.com
```

This command will stop the containers for the specified site.

   - Delete an existing WordPress site named "myblog.com":

```bash
   sudo python3 main.py delete myblog.com
```

This command deletes a WordPress site and removes all associated containers and local files and will stop and remove the containers, delete the site directory, and remove the entry from /etc/hosts.

**6.** After creating a new WordPress site, you can access it in your web browser at **'http://<site_name>'** (e.g., **'http://myblog.com'**).

## Notes

- Make sure you have the necessary permissions to install packages and make changes to system files (sudo access might be necessary). Verify that ports 80 and 443 are free on your system as they will be utilized by the Docker containers.

- If Docker and/or Docker Compose are not installed on your system, the script will attempt to install them for you. In such cases, you may be prompted to enter your password (requires `sudo` privileges).

- Before enabling, disabling, or deleting a WordPress site, ensure that the site exists (i.e., you have previously created it using the `create` command).

- The script will create a Docker Compose YAML file with a predefined LEMP stack configuration for WordPress (Linux, Nginx, MySQL, PHP). You can modify the `LEMP_TEMPLATE` variable in the script to customize the configuration according to your needs.

- Use the script responsibly and make sure to back up any important data before performing operations like deletion.

