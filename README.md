<div align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="./assets/images/DuckDB_Logo-horizontal.svg">
    <source media="(prefers-color-scheme: dark)" srcset="./assets/images/DuckDB_Logo-horizontal-dark-mode.svg">
    <img alt="DuckDB logo" src="./images/logo-dl/DuckDB_Logo-horizontal.svg" height="100">
  </picture>
</div>
<br>

# Duckdb Build Status

### What it is

* This repo holds the source for the public **DuckDB Nightly Build Status** site (static pages with daily updates based on nigthly builds created in [DuckDB repository](https://github.com/duckdb/duckdb)). It’s a Jekyll site using the **Just the Docs** theme.

# 

Here’s a **short maintenance guide** for **duckdb/duckdb-build-status**.

### Key layout

* Jekyll: `_config.yml`, `Gemfile`, layouts/partials (`_layouts/`, `_includes/`), styles (`_sass/`), and the landing page [`index.md`](https://github.com/duckdb/duckdb-build-status/blob/main/index.md).
* Workflow: [`NightlyBuildsCheck.yml`](https://github.com/duckdb/duckdb-build-status/blob/main/.github/workflows/NightlyBuildsCheck.yml) workflow is the entry point and it's triggered by notification from [`InvokeCI.yml`](https://github.com/duckdb/duckdb/actions/workflows/InvokeCI.yml). It uses scripts to create build reports and push them to update this repo contents. When it completes, Pages get automatically deployed.
You can re-run the `NightlyBuildsCheck` manually and if you don't want that run results to be deployed, just pass `false` to the [`shoulf_be_deployed`](https://github.com/duckdb/duckdb-build-status/blob/8545b4072c10dfff86e788cadbf8cc38081b3bbc/.github/workflows/NightlyBuildsCheck.yml#L14) input.
> ❗️ Sinse `InvokeCI` runs on different branches, its each run triggers corresponding run of the `NightlyBuildsCheck`
* Build helpers: `scripts/` with tasks to fetch/assemble data and produce generated content. ([scripts][https://github.com/duckdb/duckdb-build-status/tree/main/scripts])
* Generated content: dated pages like `docs/main/YYYY-MM-DD-main.md`. ([`docs/main`](https://github.com/duckdb/duckdb-build-status/tree/main/docs/main))

### Run the site locally

```bash
# in the repo root
bundle install
bundle exec jekyll serve
# open http://127.0.0.1:4000
```

### Typical maintenance

* **When new release branch** in the main DuckDB repo, create a corresponding branch in current repo to trigger nighly builds status report creation for the **new** branch of **DuckDB**. Web-site structure and [`create_inputs()`](https://github.com/duckdb/duckdb-build-status/blob/fb1b1803e64dfa593e096f384282e372aba754d3/scripts/create_tables_and_inputs.py#L361) should also be updated.

* **If InvokeCI trigger changes**, it doesn't matter for the auto daily run, but when you'd like to re-run `NightlyBuildsCheck` workflow manually, you should use new event name for the `event` input. ([NightlyBuildsCheck](https://github.com/duckdb/duckdb-build-status/blob/main/.github/workflows/NightlyBuildsCheck.yml#L12))

If you tell me which branches/dates you plan to keep on the site, I can draft a minimal “one-button” Rake command (or a short shell script) tailored to just those inputs.

### Updating repository tree, when there is a new release branch in `duckdb/duckdb` 
1. `mkdir docs/<new branch name>`, e.g. `mkdir docs/v1.4-andium`
2. Create for copy+paste and rename one of `.md` files in `docs` directory to create `.md` file for the new release, e.g. `docs/andium.md` - this will be a page template serving a list of the build reports for that branch
3. Change navigation order in all `docs/*.md` files as you think it will work best, remember that `main` should have always `nav_order: 1`.
4. Merge these updates to `main` - if `docs/v1.4-andium` doesn't exist, it will fail on pushing reports and will not deploy the Pages for that branch.

##### Powered by [Just the docs](https://just-the-docs.com/) theme for Jekyll.
