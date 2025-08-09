# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Fixed
- **Host Component States**: Fixed `get_host_details` function to properly retrieve and display component states (STARTED/STOPPED/INSTALLED) instead of showing all components as "UNKNOWN"
  - Added proper API fields parameter to request component state information
  - Component states now correctly show service-specific status for each host
  - Improved component state summary with accurate counts by status

### Improved
- Enhanced host details output with accurate component state information
- Better service grouping and state indicators in host component listing
- More reliable component status tracking across all hosts

## Previous Versions
See Git history for changes prior to this changelog.
