# museLibSys

Music Library Application is a web app inspired by Spotify for managing songs, albums, artists, personal libraries and playlists, backed by an 11-table PostgreSQL schema on Supabase.

CSE 412 Database Management, Fall 2026, Group 39.

## Tech stack

- Python 3.10+ and Flask
- PostgreSQL hosted on Supabase, accessed with raw SQL through psycopg 3
- Jinja templates and plain CSS

## Setup

1. Clone the repository and enter it.

   ```bash
   git clone https://github.com/teresakatu/museLibSys.git
   cd museLibSys
   ```

2. Create a virtual environment and install dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   On Windows, activate with `venv\Scripts\activate`.

3. Create the database. In the Supabase dashboard, open **SQL Editor** and run `db/01_schema.sql`, then `db/02_data.sql`. With a local PostgreSQL instead:

   ```bash
   createdb mla
   psql -d mla -f db/01_schema.sql -f db/02_data.sql
   ```

4. Configure environment variables.

   ```bash
   cp .env.example .env
   ```

   Set `DATABASE_URL` to the **Session pooler** connection string from Supabase (**Connect** button at the top of the project), and set `SECRET_KEY` to any long random string. Never commit `.env`.

5. Run the app.

   ```bash
   python app.py
   ```

   Open http://127.0.0.1:5000 and sign up, or log in as a sample listener such as `tnguyen` / `Lotus!Beats4`.

## Project structure

```
app.py            Flask app factory and entry point
db.py             Database connection and query helpers
routes/           One blueprint per area of the app
templates/        Jinja HTML templates
static/           CSS
db/               Schema, sample data and reference queries
```
