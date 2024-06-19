# Changelog

All notable changes to this project will be documented in this file.

## [0.5.0]

### Added

- Sentry configuration for better exception tracking

### Modified

- Exception handling in API
- Move functions to `services` and `utils` modules to differentiate business logic
- Pydoc strings to make them uniform
- Add unit tests related to `services` and `utils`
- Replace `matplotlib` `set_tight_layout()` with `set_layout_engine` due to deprecation
- Replace `config` by `Settings` class for better settings organization

## [0.4.4] - 11/06/2024

### Fixed

- Documentation styles when deployed under base path

## [0.4.3] - 29/05/2024

### Added

- `BASE_PATH` environment variable to set a prefix for endpoints

## [0.4.2] - 21/05/2024

### Modified

- Remove option Y-up to keep original coordinates

## [0.4.1] - 12/05/2024

### Fixed

- Fix pipeline pushing in Dockerhub failing due to lack of memory

## [0.4.0] - 06/05/2024

### Added

- NeuroMorphoVis integration for soma reconstruction

### Modified

- Downgrade Python version to `3.10` to support dependencies

## [0.3.0] - 05/04/2024

### Removed

- Server configuration folder

### Modified

- Folder structure to include only `/api`
- Installation to use `poetry`
- Python version to `3.12`

## [0.2.3] - 12/02/2024

### Fixed

- Dockerhub image deployment path

## [0.2.2] - 07/02/2024

### Added

- CI job to deploy service in Dockerhub

## [0.2.1] - 30/01/2024

### Fixed

- Ephys plot images not closing (memory issue)

## [0.2.0] - 25/01/2024

### Added

- Endpoint for generating electrophysiology trace images
- Environment variables in docker-compose

## [0.1.1] - 16/01/2024

### Added

- Whitelisted CORS URLs as environment variables
- README.md file

## [0.1.0] - 15/01/2024

### Added

- Initialize FASTAPI application
- Add Gitlab CI pipeline to lint, test and deploy
- Add NGINX server to enable caching
- Add black and pylint linters
