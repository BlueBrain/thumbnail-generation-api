# Changelog

All notable changes to this project will be documented in this file.


## [0.2.4] - 12/02/2024

### Removed

- Server configuration folder

### Modified

- Folder structure to include only `/api`
- Installation to use `poetry`


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

