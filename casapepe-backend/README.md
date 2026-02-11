# Casa Pepe Backend

## Setup

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Set up environment variables:
    - Ensure `.env` exists with `AIRTABLE_API_KEY` and `AIRTABLE_BASE_ID`.

## Running the Server

```bash
python server.py
```

The server will run on `http://localhost:5000`.

## Endpoints

### POST /api/restaurantes/search
Search for restaurants.
**Body:** `{"query": "name"}`

## Testing

```bash
pytest
```
