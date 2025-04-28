import paramiko , json

" USED sudo debootstrap jammy ./myrootfs http://archive.ubuntu.com/ubuntu/ to create a minimal Ubuntu root filesystem for 'jammy' (codename for the Ubuntu 22.04 LTS release)"


def get_directory_tree(ssh_client, remote_path):
    """
    Recursively fetches the directory structure from a remote machine using SSH.
    """
    directory_tree = {}

    stdin, stdout, stderr = ssh_client.exec_command(f"ls -l {remote_path}")
    output = stdout.readlines()

    for line in output:
        parts = line.split()
        if parts[0].startswith('d'):  # This is a directory
            dir_name = parts[-1]
            dir_path = f"{remote_path}/{dir_name}"

            # Recursively fetch the contents of the directory
            directory_tree[dir_name] = get_directory_tree(ssh_client, dir_path)

        elif parts[0].startswith('-'):  # This is a file
            file_name = parts[-1]
            directory_tree[file_name] = None  # or if its an important file the value should point to the files/filename"

    with open('directory_tree.json', 'w') as f:
        json.dump(directory_tree, f)
    return directory_tree

def print_directory_tree(directory_tree, indent=0):

    for key, value in directory_tree.items():
        print('  ' * indent + key)
        if isinstance(value, dict):  # If it's a directory, call the function recursively
            print_directory_tree(value, indent + 1)

def main():
    hostname = "......"  
    port = 22 
    username = "......"
    password = "....."  

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, port=port, username=username, password=password)

    remote_path = "~/myrootfs"

    directory_tree = get_directory_tree(ssh_client, remote_path)

    print_directory_tree(directory_tree)

    ssh_client.close()

if __name__ == "__main__":
    main()
