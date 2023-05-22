# tap-adobe-umapi

`tap-adobe-umapi` is a Singer tap for the [Adobe User Management API](https://developer.adobe.com/UMAPI/).

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps and the [Adobe User Management API Reference](https://adobe-apiplatform.github.io/umapi-documentation/en/)

<!--

Developer TODO: Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

## Installation

Install from PyPi:

```bash
pipx install tap-adobe-umapi
```

Install from GitHub:

```bash
pipx install git+https://github.com/ORG_NAME/tap-adobe-umapi.git@main
```

-->

Install from GitHub:

```bash
pipx install git+https://github.com/Slalom-Consulting/tap-adobe-umapi.git@main
```

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`

## Configuration

### Accepted Config Options

<!--
Developer TODO: Provide a list of config options accepted by the tap.

This section can be created by copy-pasting the CLI output from:

```
tap-adobe-umapi --about --format=markdown
```
-->

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| client_id           | True     | None    | The Client ID for the service account (JWT). |
| client_secret       | True     | None    | The Client Secret for the service account (JWT). |
| technical_account_id| True     | None    | The Technical Account ID for the service account (JWT). |
| private_key         | True     | None    | The Private Key for the service account (JWT). |
| organization_id     | True     | None    | The unique identifier for an organization. |
| auth_expiration     | False    |     300 | Expiraton in seconds for JWT exchange (Max: 86400, Recomended as small as possible). |
| user_agent          | False    | None    | User agent to present to the API. |
| api_url             | False    | None    | Override the Adobe User Management API base URL. |
| stream_config       | False    | None    | Specify additional configurations for a specified stream |

A full list of supported settings and capabilities for this tap is available by running:

```bash
tap-adobe-umapi --about
```

### Settings for Specific Streams

Settings can be added on a per-stream basis and can be set using the stream_config setting. The stream_config setting takes a dictionary with the stream name as the key and supports the following configuration options:

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| parameters          | False    | None    | URL query string to send to the stream endpoint |

Example:

```json
{
    "stream_config": {
        "users": {
            "parameters": "?domain=false&directOnly=false"
        }
    }
}
```

### Source Authentication and Authorization

Required auth configuration can be found [here](https://developer.adobe.com/developer-console/docs/guides/authentication/ServiceAccountIntegration/).

### Executing the Tap Directly

```bash
tap-adobe-umapi --version
tap-adobe-umapi --help
tap-adobe-umapi --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_adobe_umapi/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap_adobe_umapi` CLI interface directly using `poetry run`:

```bash
poetry run tap-adobe-umapi --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-adobe-umapi
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-adobe-umapi --version
# OR run a test `elt` pipeline:
meltano elt tap-adobe-umapi target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
