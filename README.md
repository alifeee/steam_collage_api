# Steam Collage

Makes a collage image out of your steam games using python.

Example: ![Collage image](./images/alifeee.png)

## API Development

This is a python script which uses Flask to serve an API for getting a collage image.

### API Key

A steam API key must be placed in the files `api_key.txt` and `.env` in the root directory. Keys can be obtained from [Steam](https://steamcommunity.com/dev/apikey).

#### `api_key.txt`

```text
8917981789178
```

#### `.env`

```text
API_KEY=8917981789178
```

### Commands

#### Use python virtual environment

```bash
python -m venv env
```

#### Install modules from requirements.txt

```bash
pip install -r requirements.txt
```

#### Save modules to requirements.txt

```bash
pip freeze > requirements.txt
```

#### Run tests

```bash
ptw
```

#### Run server

```bash
python ./api/api.py
```

### API

#### GET `/steamcollage/games`

Returns a list of games for a given steam ID.

##### Parameters

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `string` | Steam ID or vanity URL of the user, e.g., alifeee |
| `cols` | `int` | Number of columns in the collage |
| `rows` | `int` | Number of rows in the collage |
| `sort` | `name`, `recent`, or `playtime` | Sort order of the games |

##### Example

```bash
curl http://localhost:5000/steamcollage/games?id=alifeee&cols=5&rows=5&sort=recent
```
