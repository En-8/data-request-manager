all:
  hosts:
    api:
      ansible_host: ${ec2_public_ip}
      ansible_user: ${ssh_user}
      ansible_ssh_private_key_file: ${ssh_key_path}
