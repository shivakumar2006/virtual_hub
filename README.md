# Virtual Hub - Home Assistant Custom Integration

## Overview

Virtual Hub is a custom Home Assistant integration that simulates a centralized media control system for multiple entertainment devices.

The integration creates and manages all entities internally and provides a single hub that controls and coordinates:

- TV
- AVR (Audio Video Receiver)
- Apple TV
- Music System
- Game Console

The integration demonstrates:

- Config Flow implementation
- Integration-managed entities
- State synchronization
- Source routing
- Playback management
- Volume control
- Dynamic Home Assistant UI updates

No entities are manually defined through YAML. All entities are created and managed by the integration itself.

---

## Features

### Config Flow

The integration supports Home Assistant's UI-based setup flow.

Users can create a new Virtual Hub by providing:

- Mock IP Address
- Mock OTP / Pairing Code

### OTP Validation

Mock authentication logic is implemented.

#### Valid OTP

```text
123456
```

#### Invalid OTP

Any other OTP value is rejected and the setup flow displays an error.

---

### Duplicate IP Handling

The integration prevents duplicate hub creation.

If a hub with the same IP address already exists:

- Setup is aborted
- User receives a duplicate configuration error

This ensures that only one Virtual Hub can exist per IP address.

---

## Entities Created

When the integration is configured, it automatically creates the following entities:

### Hub

```text
Virtual Hub
```

### Media Devices

```text
TV
AVR
Apple TV
Music System
Game Console
```

All entities are created dynamically by the integration.

No manual entity configuration is required.

---

## Architecture

```text
Virtual Hub
├── TV
├── AVR
├── Apple TV
├── Music System
└── Game Console
```

### Infrastructure Devices

The following devices are considered infrastructure components:

```text
TV
AVR
```

### Source Devices

The following devices act as content sources:

```text
Apple TV
Music System
Game Console
```

Only one source device can be active at a time.

---

## Hub Behavior

The Virtual Hub acts as the master controller.

### Power On

When the hub is powered on:

```text
TV → ON
AVR → ON
```

Source devices remain inactive until selected.

---

### Power Off

When the hub is powered off:

```text
TV → OFF
AVR → OFF
Apple TV → OFF
Music System → OFF
Game Console → OFF
```

The active source is cleared and playback returns to idle.

---

## Source Routing

The integration maintains a single active source.

### Example

Selecting:

```text
Apple TV
```

results in:

```text
TV → ON
AVR → ON
Apple TV → ON
Music System → OFF
Game Console → OFF
```

and:

```text
active_source = Apple TV
```

---

Selecting:

```text
Music System
```

results in:

```text
TV → ON
AVR → ON
Apple TV → OFF
Music System → ON
Game Console → OFF
```

and:

```text
active_source = Music System
```

Only one source may be active at any time.

---

## Playback Management

The hub maintains playback state.

Supported states:

```text
idle
playing
paused
```

Playback controls are exposed through Home Assistant and automatically update integration state.

---

## Volume Management

The AVR entity exposes volume controls.

Supported functionality:

- Volume Adjustment
- Volume State Tracking
- Dynamic UI Updates

Volume changes are reflected immediately in Home Assistant.

---

## State Synchronization

The integration uses an internal manager to coordinate all devices.

Whenever a device state changes:

- Hub state updates
- Active source updates
- Playback state updates
- Device states synchronize automatically

The Home Assistant UI reflects changes in real time.

---

## Hub Attributes

The Virtual Hub exposes additional state information.

Examples:

```yaml
active_source: Apple TV
system_ready: true
playback_state: playing
avr_volume: 25
playback_available: true
hub_power: true
device_count: 5
```

---

## Installation

### Manual Installation

Copy the integration into:

```text
config/custom_components/virtual_hub
```

Example:

```text
config/
└── custom_components/
    └── virtual_hub/
```

Restart Home Assistant.

---

### Add Integration

Navigate to:

```text
Settings
→ Devices & Services
→ Add Integration
→ Virtual Hub
```

Enter:

```text
IP Address
OTP Code
```

Complete setup.

---

## Testing Scenarios

### Valid Setup

```text
IP: 192.168.1.10
OTP: 123456
```

Expected Result:

```text
Integration Added Successfully
```

---

### Invalid OTP

```text
OTP: 000000
```

Expected Result:

```text
Setup Fails
Invalid OTP Error Displayed
```

---

### Duplicate IP

Attempt to configure the same IP twice.

Expected Result:

```text
Configuration Aborted
Duplicate Hub Detected
```

---

### Source Switching

```text
Apple TV → Music System
```

Expected Result:

```text
Apple TV OFF
Music System ON
active_source updated
```

---

### Hub Shutdown

```text
Virtual Hub OFF
```

Expected Result:

```text
All devices OFF
active_source cleared
playback reset
```

---

## Design Goals

This integration was built to demonstrate:

- Home Assistant Custom Integration Development
- Config Flow Implementation
- Dynamic Entity Creation
- State Management
- Entity Synchronization
- Hub-Based Device Coordination
- Integration-Driven UI Updates

---

## Future Improvements

Potential enhancements include:

- State persistence across Home Assistant restarts
- Additional media device types
- Multiple Virtual Hub instances
- Advanced routing rules
- Mock network discovery
- Coordinator-based update architecture

---

## Author

Shiva

Home Assistant Custom Integration Assignment
