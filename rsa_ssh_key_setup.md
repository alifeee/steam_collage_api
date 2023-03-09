# RSA Key Setup

This describes the process of setting up a new user on a server with an RSA key. The user is able to control docker, and can log in to the server without a password. This enables us to use GitHub Actions to deploy our docker images to the server using SSH.

## Help Links

- <https://nbailey.ca/post/github-actions-ssh/>
- <https://www.christopherbiscardi.com/copy-an-extra-key-to-a-digital-ocean-droplit>
- <https://www.christopherbiscardi.com/deploying-docker-images-to-digital-ocean-without-a-registry-via-git-hub-actions>
- <http://www.linuxproblem.org/art_9.html>

## Server actions

```bash
ssh root@45.91.169.110
```

### Make new user

```bash
sudo useradd --create-home --user-group --shell /bin/bash --groups docker deploy
sudo usermod --lock deploy
```

### Switch to new user

```bash
sudo -i -u deploy
```

### Make an ssh key

```bash
$ ssh-keygen -f ~/.ssh/id_ed25519 -C "deploy@server"
> [no password]
```

### Gopy key to authorised keys

```bash
cat .ssh/id_ed25519.pub > .ssh/authorized_keys
```

## Client actions

### Get ssh private key

```bash
scp root@45.91.169.110:/home/deploy/.ssh/id_ed25519 C:\Users\alifeee\.ssh
```

### login with key (password not required)

```bash
ssh -i C:\Users\alifeee\.ssh\id_ed25519 deploy@45.91.169.110
```
