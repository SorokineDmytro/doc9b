# Doc9b

Doc9b is a Django documentation/wiki-style app to organize content by:
- `Space` (top-level area)
- `Page` (hierarchical pages with parent/children)
- `UserCategory` (page categorization)

The UI includes:
- a space list page
- a space details page with root pages
- a page details view with breadcrumbs and child navigation

## Tech stack

- Python `>=3.13`
- Django `6.0.2`
- SQLite (default local database)

## Project structure

- `docneufb/` Django project config (`settings.py`, root `urls.py`)
- `docs/` main app (`models.py`, `views.py`, `urls.py`, `admin.py`)
- `templates/` HTML templates
- `static/css/styles.css` styles

## Data model

### `Space`
- `name` (unique)
- `slug` (auto-generated from name if empty)
- `description`
- `created_at`, `updated_at`

### `Page`
- belongs to one `Space`
- optional self-relation `parent` (for nested pages)
- `title`, `slug`, `content`, `order`
- many-to-many with `UserCategory`
- unique constraint on `(space, slug)`

### `UserCategory`
- `name` (unique)
- `slug` (auto-generated if empty)

## Routes

- `/` -> list all spaces
- `/<space_slug>` -> space details and root pages
- `/<space_slug>/<page_slug>` -> page details + breadcrumbs + children
- `/admin/` -> Django admin

## Local setup

### 1. Clone and enter project

```bash
git clone git@github.com:SorokineDmytro/doc9b.git
cd doc9b
```

### 2. Configure environment

`SECRET_KEY` is read from .env in the project's root.


### 3. Install dependencies

With `uv`:

```bash
uv sync
```

Or with `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "django>=6.0.2"
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. (Optional) Create admin user

```bash
python manage.py createsuperuser
```

### 6. Start development server

```bash
uv run --env-file .env ./manage.py runserver
```

Open `http://127.0.0.1:8000/`.
