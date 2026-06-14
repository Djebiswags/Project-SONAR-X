# TECHNICAL_SPEC.md

## System Overview
Project SONAR-X is a persistent, non-intrusive system daemon designed for high-performance macOS environments. It utilizes `launchd` for process management, ensuring system-level persistence for telemetry 
operations.

## Architectural Pillars
* **Decoupled Architecture**: Separation of concerns between the background telemetry daemon and the front-end visualization layer via `CustomTkinter`.
* **Asynchronous Telemetry**: Implements an asynchronous heartbeat loop to monitor system health without impacting user workflows.
* **Defensive Automation**: Configurable `kill_list` targeting background process overhead to maintain system responsiveness during high-load periods.

## Deployment & Security
* **Persistence**: Leverages user-level `LaunchAgents` for automated daemon initialization on boot.
* **Resource Integrity**: Employs absolute-path referencing and script-wrapper abstraction to ensure environment consistency within isolated Python virtual environments.
