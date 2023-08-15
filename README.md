# Steam Collage API

An API to generate a collage of games from a Steam profile. Python is used to generate the image, which is served via an HTTP server using [Flask](https://flask.palletsprojects.com/en/2.2.x/). Hosted using [Kamatera](https://console.kamatera.com/).

![Collage image](./images/alifeee.png)

## URLs

| Service | URL |
| -------- | --- |
| Docker Hub | [alifeee/steamcollageapi](https://hub.docker.com/repository/docker/alifeee/steamcollageapi) |
| GitHub | [alifeee/steam_collage](https://github.com/alifeee/steam_collage/) |
| Kamatera Console | [alifeee](https://console.kamatera.com/) |
| Kamatera Server | 45.91.169.110 |

## Environment

A .env file is used to store environment variables. The following variables are used:

| Name | Description |
| ---- | ----------- |
| `API_KEY` | Steam API key - see [below](#api-key). |
| `DO_CACHE` | Whether to cache the game thumbnails. Note that this increases the memory usage of the server. |

```text
# .env
API_KEY=8917981789178
DO_CACHE=True
```

### API Key

A steam API key must be placed in the `.env` file in the root directory, or exposed to the environment via the terminal. Keys can be obtained from [Steam](https://steamcommunity.com/dev/apikey).

## Commands

### Use python virtual environment

```bash
python -m venv env
```

### Install modules from requirements.txt

```bash
pip install -r requirements.txt
```

### Save modules to requirements.txt

```bash
pip freeze > requirements.txt
```

### Run tests

```bash
ptw -- --cov=api
```

### Run server locally

```bash
python ./api/api.py debug
```

### Build and run docker image

```bash
docker build -t alifeee/steamcollageapi .
docker run -p 5000:5000 -e API_KEY=8917981789178 alifeee/steamcollageapi
```

### Push docker image to Docker Hub

```bash
docker push alifeee/steamcollageapi
```

## Thunder Client

Thunder client is a VS Code extension which allows you to make HTTP requests. It is useful for testing the API.

### Testing

Some tests are included in the `tests` collection. These can be run by using the `Run All` button in the top right of collection.

## Deploying to Kamatera (remote)

### Connect to Kamatera

```bash
ssh root@45.91.169.110
> enter password
```

### Pull the latest image from Docker Hub

```bash
docker pull alifeee/steamcollageapi
```

### Remove existing container

```bash
docker ps -a
> get container id
docker rm <container id>
```

### Run image

```bash
docker create -p 5000:5000 -e API_KEY=8917981789178 alifeee/steamcollageapi
> get container id
docker start <container id>
```

## GitHub actions

### `python-app.yml`: Python testing

This workflow:

1. Checks out the repository
2. Sets up Python 3.10
3. Installs dependencies
4. Runs linting
5. Runs tests

#### Secrets

None.

### `docker-image.yml`: Docker

This workflow:

1. Checks out the repository
2. Builds the Docker image
3. Pushes the Docker image to Docker Hub
4. Deploys the Docker image to Kamatera

#### Secrets used for Docker and Kamatera

| Name | Description |
| ---- | ----------- |
| `API_KEY` | Steam API key - see [above](#api-key). |
| `DOCKERHUB_USERNAME` | Docker Hub username. |
| `DOCKERHUB_TOKEN` | [Docker Hub access token](https://docs.docker.com/docker-hub/access-tokens/). |
| `HOST` | IP address of the Kamatera server |
| `USERNAME` | Username for the Kamatera server |
| `KEY` | RSA key* for the Kamatera server |

##### *RSA key

See [rsa_ssh_key_setup.md](./rsa_ssh_key_setup.md) for details on setting up the RSA key.

## API

All APIs are served on the port `5000`.

### GET `/steamcollage/games`

Returns a list of games for a given steam ID.

#### Query Parameters {1}

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `string` | Steam ID or vanity URL of the user, e.g., alifeee |
| `cols` | `int` | Number of columns in the collage |
| `rows` | `int` | Number of rows in the collage |
| `sort` | `name`, `recent`, or `playtime` | Sort order of the games |

```bash
wget http://localhost:5000/steamcollage/games?id=alifeee&cols=5&rows=5&sort=recent
```

![Example image which would be generated by the above API](images/api_collage.png)

### GET `/steamcollage/verifyuser`

Returns a boolean indicating whether a given steam account exists, and whether it is private.

#### Query Parameters {#2}

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `string` | Steam ID or vanity URL of the user, e.g., alifeee |

```bash
wget http://localhost:5000/steamcollage/verifyuser?id=alifeee
```

```json
{
  "exists": true,
  "private": false
}
```

### GET `/steamcollage/alive`

Returns "Alive" if the server is running.

```bash
wget http://localhost:5000/steamcollage/alive
```

```text
"Alive"
```

### GET `/steamcollage/alive_img`

Returns an image if the server is running.

```bash
wget http://localhost:5000/steamcollage/alive_img
```

![Lovely picture of a sheep](./sheep.png)

## Alive check

To check the API is alive, I use [Testfully] to poll the `/steamcollage/alive` endpoint every hour.

[Testfully]: https://app.testfully.io
