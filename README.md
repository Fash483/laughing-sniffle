# ✦ Magnet Vault ✦

A React + Vite torrent magnet-link manager, backed directly by **Supabase**
(Postgres + auto-generated REST API), deployed as a static site on
**GitHub Pages**. The frontend talks to Supabase straight from the browser
using the `@supabase/supabase-js` client — no custom backend server
required.

## Quick start

```bash
npm install
cp .env.example .env   # paste your Supabase URL + anon key
npm run dev             # Vite dev server on :5173
```

## 1. Set up Supabase

1. Create a project at [supabase.com](https://supabase.com).
2. Open the **SQL Editor** and run the contents of `supabase/schema.sql`.
   This creates the `links` table and Row Level Security policies that allow
   public read/insert/delete via the anon key (suitable for a single-user /
   personal vault — see the note in that file if you want to lock it down
   with Supabase Auth instead).
3. Go to **Project Settings → API** and copy the **Project URL** and
   **anon public key**.

## 2. Configure environment variables

Copy `.env.example` to `.env` and fill in:

```
VITE_SUPABASE_URL=https://your-project-ref.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

These are safe to expose to the browser — they're the public anon key, and
access is controlled by the RLS policies in `supabase/schema.sql`. Never put
the `service_role` key in frontend code.

## 3. Deploy to GitHub Pages

The repo includes a GitHub Actions workflow
(`.github/workflows/deploy.yml`) that builds the Vite app and publishes
`dist/` to GitHub Pages on every push to `main`.

1. Push this repo to GitHub.
2. In the repo: **Settings → Pages → Source**, select **GitHub Actions**.
3. In **Settings → Secrets and variables → Actions → New repository
   secret**, add:
   - `VITE_SUPABASE_URL` = `https://your-project-ref.supabase.co`
   - `VITE_SUPABASE_ANON_KEY` = `your-anon-key`
4. Push to `main` (or run the workflow manually from the **Actions** tab).
   The app deploys to `https://<your-username>.github.io/<repo-name>/`
   (or your custom domain, if configured under **Settings → Pages**).

Two things this app needed to work on Pages, both already handled:

- `vite.config.ts` sets `base: "./"` so built asset URLs resolve
  correctly whether the site lives at the domain root or under a
  `/<repo-name>/` subpath — GitHub Pages project sites use the latter.
- The workflow copies `dist/index.html` to `dist/404.html` after the
  build. GitHub Pages has no server-side rewrites, so this is the
  standard trick to keep deep links from 404ing (this app doesn't use
  client-side routing yet, but it's a safe default if that changes).

## Data model

Table: `public.links`

| Column     | Type        |
| ---------- | ----------- |
| id         | bigint (PK) |
| title      | text        |
| magnet     | text        |
| created_at | timestamptz |

## What changed vs. the Fly.io/Postgres version

- Removed the Express server (`server/index.js`) and Dockerfile/`fly.toml` —
  there's no custom backend anymore.
- The frontend now calls Supabase directly via `@supabase/supabase-js`
  (see `src/supabaseClient.ts`), instead of hitting a same-origin `/api/*`
  Express API.
- Deployment target: GitHub Pages via a GitHub Actions workflow
  (`.github/workflows/deploy.yml`), with a relative Vite `base` and a
  `404.html` SPA fallback, instead of a Fly.io container.
- Database: Supabase Postgres (with RLS policies) instead of Fly Postgres /
  plain `pg`.
