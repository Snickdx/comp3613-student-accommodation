# COMP 3613 Student Accommodation (Phase 2 starter)

Flawed baseline **0.2.0** built on [uwidcit/faststart](https://github.com/uwidcit/faststart) (`96ccfce`).

FastStart provides the SSR shell, JWT cookie auth, SQLModel, `manage.py`, and Render/Docker wiring. The student-accommodation scenario adds domain models/services and a JSON API under `/api` (see `/docs`).

## Quick start

```text
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Windows: Copy-Item .env.example .env
python manage.py init
python manage.py run
```

Open http://127.0.0.1:5000 — SSR auth shell; scenario JSON under `/api` and OpenAPI at `/docs`.

## Seeded API accounts

| Email | Password | Role |
| --- | --- | --- |
| `admin@example.com` | `admin-dev` | admin |
| `student@example.com` | `stud-dev` | student (registered ID) |
| `incoming@example.com` | `stud-dev` | student (provisional incoming) |
| `landlord@example.com` | `land-dev` | landlord |
| `landlord2@example.com` | `land-dev` | landlord |

JSON login: `POST /api/auth/login` with `{"email","password"}`. Other scenario endpoints identify the caller with the `X-User-Id` header (demo auth).

## Student brief

See [`ASSIGNMENT.md`](ASSIGNMENT.md) and [`docs/ACCEPTANCE.md`](docs/ACCEPTANCE.md).

## Tests

```bash
python -m pytest tests -q
```
