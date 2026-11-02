# Brazilian Climatology Data Warehouse

Python application that collects, processes, stores, and serves Brazilian climate data through a REST API.

It combines historical weather station observations from [INMET](https://portal.inmet.gov.br/dadoshistoricos) with city weather forecasts from CPTEC/INPE, stores them in PostgreSQL, and exposes query endpoints for stations, cities, historical series, averages, and forecasts.

## Features

- Interactive CLI (`main.py`) for data pipeline and API startup
- Download and process INMET historical station data (from year 2000 onward)
- Compute daily, weekly, and monthly historical averages
- Load processed historical data into PostgreSQL
- Update forecast data using IBGE localities, Google Geocoding, and CPTEC/INPE XML services
- REST API with CORS enabled for stations, cities, weather types, history, and forecasts
- One-step database bootstrap from the included full `banco_de_dados.backup` seed (enough data to run and test the API)

## Technologies

| Area | Stack |
| --- | --- |
| Language | Python |
| API | Flask, Flask-RESTful, Flask-Cors |
| Database | PostgreSQL, Peewee ORM, psycopg2 |
| Data collection | Selenium + ChromeDriver (INMET downloads), Requests, xmltodict |
| Configuration | python-dotenv (`.env`) |

## Project structure

```text
.
├── main.py                 # CLI entry point
├── API.py                  # Flask API registration and server start
├── banco_de_dados.backup   # Full PostgreSQL seed backup for local testing
├── requirements.txt
├── classes/                # Shared HTTP utilities
├── database/               # Peewee models and database restore logic
├── extract_data/           # Historical and forecast ETL
├── serve_data/             # API controllers, validation, and response formatting
└── utils/                  # Helpers and shared constants
```

## Prerequisites

- Python 3
- PostgreSQL, with `pg_restore` available on your system `PATH`
- Google Chrome (required only for menu option 1 — historical data download via Selenium)
- A Google Geocoding API key (required only for forecast updates that reload city coordinates)

## Installation

1. Clone the repository and enter the project directory.
2. Create and activate a virtual environment (recommended).
3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Create a `.env` file in the project root (see [Environment variables](#environment-variables)).

## Environment variables

Configuration is loaded from a `.env` file via `python-dotenv`. Example:

```env
# Database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=brazilian_climatology

# File processing
DEFAULT_ENCODING=latin-1
INPUT_SEPARATOR=;
OUTPUT_SEPARATOR=;
MAX_LINES_OUTPUT_FILES=100000

# External services (forecast pipeline)
BASE_URL_IBGE=https://servicodados.ibge.gov.br/api/v1
BASE_URL_GEOCODING=https://maps.googleapis.com/maps/api/geocode/json
API_KEY_GEOCODING=your_google_geocoding_api_key
BASE_URL_CPTEC=http://servicos.cptec.inpe.br/XML
```

| Variable | Purpose |
| --- | --- |
| `DATABASE_HOST` | PostgreSQL host |
| `DATABASE_PORT` | PostgreSQL port |
| `DATABASE_USER` | PostgreSQL user |
| `DATABASE_PASSWORD` | PostgreSQL password |
| `DATABASE_NAME` | Target database name |
| `DEFAULT_ENCODING` | Encoding used when reading/writing processed files |
| `INPUT_SEPARATOR` | Column separator for raw historical input files |
| `OUTPUT_SEPARATOR` | Column separator for processed output files |
| `MAX_LINES_OUTPUT_FILES` | Maximum lines per processed output file before splitting |
| `BASE_URL_IBGE` | Base URL for IBGE locality API |
| `BASE_URL_GEOCODING` | Base URL for Google Geocoding API |
| `API_KEY_GEOCODING` | Google Geocoding API key |
| `BASE_URL_CPTEC` | Base URL for CPTEC/INPE forecast XML services |

## How to run

Start the interactive menu:

```bash
python main.py
```

### Menu options

| Option | Action |
| --- | --- |
| `1` | Download historical data from INMET |
| `2` | Process downloaded historical data (optional state filter) |
| `3` | Upload processed historical data to the database |
| `4` | Update weather forecast data (optional reuse of cities already in the database; optional state filter) |
| `5` | Start the API server |
| `6` | Create the database and restore `./banco_de_dados.backup` |

### First-time setup

1. Configure `.env`.
2. Ensure PostgreSQL is running.
3. Run `python main.py` and choose **`6 - Iniciar banco de dados`** to create the database and restore the full seed backup (`banco_de_dados.backup`). This is enough to run and test the API without downloading or processing new data first.
4. Run `python main.py` again and choose **`5 - Iniciar servidor da API`**.

The API starts with Flask’s default settings (`http://127.0.0.1:5000`). Stop it with `CTRL + C`.

## API endpoints

All endpoints below are `GET` requests.

### General

| Endpoint | Description | Parameters |
| --- | --- | --- |
| `/` | Health-style root endpoint (HTTP 200) | — |
| `/station` | Stations that have historical data, grouped by state | `state` (optional UF, e.g. `SC`) |
| `/city` | Cities that have forecast data, grouped by state | `state` (optional UF) |
| `/weather-type` | Weather condition codes and descriptions | — |

Examples:

```text
http://localhost:5000/station?state=SC
http://localhost:5000/city?state=SC
http://localhost:5000/weather-type
```

### Historical data

| Endpoint | Description | Required parameters | Optional |
| --- | --- | --- | --- |
| `/history/station` | Hourly history for one station | `init_date`, `station` | `times_of_day` |
| `/history/state` | Hourly history for all stations in a state | `init_date`, `state` | `times_of_day` |
| `/history/average/station` | Daily/weekly/monthly averages for one station | `init_date`, `station`, `frequency` | — |
| `/history/average/state` | Daily/weekly/monthly averages for a state | `init_date`, `state`, `frequency` | — |

Notes:

- `init_date` format: `DD/MM/YYYY`
- `frequency` values: `daily`, `weekly`, `monthly`
- `station` is the station ID stored in the database

Examples:

```text
http://localhost:5000/history/station?init_date=20/03/2023&station=3&times_of_day=14
http://localhost:5000/history/state?init_date=20/03/2023&state=SC&times_of_day=14
http://localhost:5000/history/average/station?init_date=20/03/2023&station=3&frequency=monthly
http://localhost:5000/history/average/state?init_date=20/03/2023&state=SC&frequency=monthly
```

### Forecast data

| Endpoint | Description | Required parameters |
| --- | --- | --- |
| `/forecast/city` | Forecast for one city from today through `days` ahead | `city`, `days` |
| `/forecast/state` | Forecast for all cities in a state | `state`, `days` |
| `/forecast/average/city` | Precomputed 7- or 14-day average for one city | `city`, `period_day` |
| `/forecast/average/state` | Precomputed 7- or 14-day averages for a state | `state`, `period_day` |

Notes:

- `city` is the city ID stored in the database
- `period_day` values: `7` or `14`

Examples:

```text
http://localhost:5000/forecast/city?city=3&days=10
http://localhost:5000/forecast/state?state=SC&days=10
http://localhost:5000/forecast/average/city?city=3&period_day=7
http://localhost:5000/forecast/average/state?state=SC&period_day=14
```

### `times_of_day` rules

Used by `/history/station` and `/history/state`. Hours are integers from `0` to `23`.

1. Specific hours, comma-separated: `8,13,15` → 08:00, 13:00, 15:00
2. Hour ranges with a hyphen: `13-17` → 13:00 through 17:00
3. Combined form: `12,16-19` → 12:00, 16:00, 17:00, 18:00, 19:00

If `times_of_day` is omitted, all 24 hours are returned.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
