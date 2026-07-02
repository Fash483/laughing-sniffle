# ✦ Magnet Vault ✦

A React + Vite torrent magnet-link manager, backed directly by **Supabase**
(Postgres + auto-generated REST API), deployed as a static site on
**Cloudflare Pages**. The frontend talks to Supabase straight from the
browser using the `@supabase/supabase-js` client — no custom backend
server required.

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

## 3. Deploy to Cloudflare Pages

The app is a plain static SPA, so Cloudflare Pages builds it directly from
git with no extra build step.

**Option A — Cloudflare dashboard (deploy from Git)**

1. Push this repo to GitHub/GitLab.
2. In the Cloudflare dashboard: **Workers & Pages → Create → Pages →
   Connect to Git**, pick the repo.
3. Framework preset: **Vite** (or set manually):
   - Build command: `npm run build`
   - Build output directory: `dist`
4. Under **Settings → Environment variables**, add (for both Production and
   Preview):
   - `VITE_SUPABASE_URL` = `https://your-project-ref.supabase.co`
   - `VITE_SUPABASE_ANON_KEY` = `your-anon-key`
5. Deploy. Cloudflare gives you a `*.pages.dev` URL.

**Option B — Wrangler CLI**

```bash
npm install -g wrangler
wrangler login

npm run build
wrangler pages deploy dist --project-name=magnet-vault
```

For env vars with the CLI, set them once via the dashboard (Option A step 4)
or with:

```bash
wrangler pages secret put VITE_SUPABASE_URL --project-name=magnet-vault
wrangler pages secret put VITE_SUPABASE_ANON_KEY --project-name=magnet-vault
```

Note: since these are `VITE_*` vars, Vite inlines them at **build** time.
If you build locally and only `wrangler pages deploy dist`, make sure your
local `.env` has the right values before running `npm run build`. If
Cloudflare does the build (Option A), set them as build-time environment
variables in the dashboard instead.

`public/_redirects` (copied into `dist/` by Vite automatically) contains a
catch-all SPA rule — `/* /index.html 200` — so client-side routing works.

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
- Deployment target: Cloudflare Pages static hosting (`public/_redirects`)
  instead of a Fly.io container.
- Database: Supabase Postgres (with RLS policies) instead of Fly Postgres /
  plain `pg`.
