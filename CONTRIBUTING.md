# Contributing

Thanks for helping improve the Mage Python SDK. Bug reports and pull requests are welcome.

## Development

You need [uv](https://docs.astral.sh/uv/).

```bash
uv sync                          # create .venv with the SDK and dev tools
uv run pytest                    # tests (no network)
uv run ruff check                # lint
uv run ruff format               # format
uv run mypy                      # strict type check
uv run python scripts/generate.py  # regenerate types from spec/openapi.json
```

CI runs all of these on Python 3.10 to 3.14, and fails when the generated code does not match the spec.

Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages and pull request titles (`fix: ...`, `feat: ...`, `docs: ...`); releases and the changelog are built from them. Pull requests are squash-merged.

## Generated code

`src/mage_space/_generated.py` is generated from `spec/openapi.json` by `scripts/generate.py`. Never edit it by hand: change the generator (or the spec, upstream) and regenerate. The generator is standard-library Python and handles the subset of JSON Schema the spec uses; it stops with an error on anything else.

`spec/openapi.json` is a copy of https://docs.mage.space/api/openapi.json, the spec the API's documentation is built from. Do not edit it in a pull request; the sync workflow updates it.

## How the spec stays in sync

`.github/workflows/sync-spec.yml` runs every hour (and on demand). When the published spec differs from `spec/openapi.json`, it regenerates the types and opens or updates the pull request `bot/sync-spec`, titled by what the change does to clients according to [oasdiff](https://github.com/oasdiff/oasdiff):

| Title | Meaning | Merge |
| --- | --- | --- |
| `feat!: sync API spec` | Something was removed or tightened (a breaking change) | Waits for review (`needs-review` label) |
| `feat: sync API spec` | Models, fields, or options were added | Automatic once CI passes |
| `docs: sync API spec` | Wording only | Automatic once CI passes |

A model newer than the installed SDK already works by its id, so a lag here only delays its types.

## Releases

[release-please](https://github.com/googleapis/release-please) keeps a release pull request open with the next version and changelog. Merging it tags the release and `.github/workflows/release.yml` publishes to PyPI with trusted publishing. Before 1.0, a breaking change bumps the minor version and anything else the patch version. The version lives in `src/mage_space/_version.py`.

`.github/workflows/smoke.yml` runs the SDK against the real API every night (`scripts/smoke.py`, one generation with the cheapest image model) when the `MAGE_API_KEY` secret is set.

## Maintainer setup

One-time settings the workflows depend on:

- **GitHub App** installed on this repository with read and write access to contents and pull requests. Its id goes in the `MAGE_BOT_APP_ID` variable and its private key in the `MAGE_BOT_PRIVATE_KEY` secret. The sync and release workflows use its token so that CI runs on the pull requests they open.
- **Repository settings:** allow auto-merge and squash merging; protect `main` with the CI checks (`Lint and types`, `Test (Python 3.10)` to `Test (Python 3.14)`, `Build`) required.
- **PyPI trusted publisher** for the `mage-space` project: this repository, workflow `release.yml`, environment `pypi`. Create the `pypi` environment in the repository settings.
- **`MAGE_API_KEY` secret** (optional) for the nightly smoke test, from an account with a small Gem balance.
