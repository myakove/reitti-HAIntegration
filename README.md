# Reitti Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/karldonteljames/reitti-HAIntegration)](https://github.com/karldonteljames/reitti-HAIntegration/releases)
[![GitHub](https://img.shields.io/github/license/karldonteljames/reitti-HAIntegration)](LICENSE)

A Home Assistant custom integration that pushes device tracker location data to a Reitti server using the OwnTracks format.

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed
2. Go to HACS → Integrations
3. Click the menu (three dots) in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/myakove/reitti-HAIntegration`
6. Set category to "Integration"
7. Click "Add"
8. Find "Reitti Integration" in the list and install it
9. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/karldonteljames/reitti-HAIntegration/releases)
2. Extract the contents
3. Copy the `custom_components/reitti` folder to your Home Assistant `config/custom_components/` directory
4. Restart Home Assistant

## Configuration

### Through the UI

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Reitti Integration"
4. Follow the configuration wizard

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| **Reitti Server URL** | URL of your Reitti server | `http://reitti` |
| **Port** | Server port | `8080` |
| **API Key** | Your Reitti API token | *Required* |
| **Device** | Device tracker to monitor | *Required* |
| **Push Interval** | Seconds between updates | `30` |
| **Enable Push** | Enable automatic pushes | `true` |
| **Debug Logging** | Enable debug logging | `false` |
| **Friendly Name** | Display name | `Reitti Integration` |

## Features

### ✅ Automatic Location Pushing
- Pushes location data at configurable intervals
- Triggers immediate updates when device state changes
- Supports multiple device trackers with separate integrations

### ✅ Complete Reconfiguration Support
- Modify ALL settings (URL, API key, device tracker, intervals, etc.) in one form
- Access via: Integration → Three dots menu → **"Reconfigure"**
- No need to remove and re-add the integration

### ✅ Runtime Options
- Quick access to common settings (intervals, debug logging, device tracker)
- Access via: Integration → Three dots menu → **"Configure"** → **"Options"**
- No restart required for option changes

### ✅ Manual Push Service
- `reitti.push_now` service for on-demand location updates
- Useful for automation and testing

### ✅ Debug Support
- Comprehensive logging for troubleshooting
- View request/response data when debug mode is enabled

## Services

### `reitti.push_now`

Manually trigger an immediate location update.

```yaml
service: reitti.push_now
```

## Data Format

The integration sends data in OwnTracks format:

```json
{
  "_type": "location",
  "tid": "AB",
  "lat": 40.7128,
  "lon": -74.0060,
  "alt": 10,
  "acc": 5,
  "tst": 1703097600
}
```

## Troubleshooting

### Enable Debug Logging

1. Go to integration options and enable "Debug Logging"
2. Check Home Assistant logs for detailed information

### Common Issues

- **Connection refused**: Check Reitti server URL and port
- **401 Unauthorized**: Verify API token is correct
- **No location data**: Ensure device tracker has GPS coordinates
- **Rate limiting**: Increase push interval if server is overloaded

## Development

### Local Development

```bash
# Clone the repository
git clone https://github.com/karldonteljames/reitti-HAIntegration.git

# Set up development environment
cd reitti-HAIntegration
python -m venv venv
source venv/bin/activate
pip install -r requirements_dev.txt

# Run tests
python -m pytest tests/
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- [GitHub Issues](https://github.com/karldonteljames/reitti-HAIntegration/issues)
- [Home Assistant Community](https://community.home-assistant.io/)

## Changelog

### v1.0.2
- Fixed HACS download issues with zip_release configuration
- Updated release management for better HACS compatibility

### v1.0.1
- Added complete reconfiguration support for all options
- Fixed reconfigure flow to include all settings in one form
- Enhanced reconfigure to update both config data and options

### v1.0.0
- Added reconfiguration support
- Improved options flow with better validation
- Enhanced error handling
- Added HACS compatibility
- Added device tracker reconfiguration to options flow

### v0.1.4
- Fixed logging variables
- Added friendly names for better device identification
- Made API calls thread-safe
- Updated deprecation warnings
