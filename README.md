# dimstack Demo with marimo WebAssembly

## Usage

1. Add marimo files to the `notebooks/` or `apps/` directory
   1. `notebooks/` notebooks are exported with `--mode edit`
   2. `apps/` notebooks are exported with `--mode run`
2. `uv run marimo edit` to work on them
3. Push to main branch
4. Go to repository **Settings > Pages** and change the "Source" dropdown to "GitHub Actions"
5. GitHub Actions will automatically build and deploy to Pages

## Testing

To test the export process, run `scripts/build.py` from the root directory.

```bash
uv run python scripts/build.py
```

This will export all notebooks in a folder called `_site/` in the root directory. Then to serve the site, run:

```bash
uv run python -m http.server -d _site
```

This will serve the site at `http://localhost:8000`.
