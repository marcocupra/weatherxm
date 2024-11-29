# WeatherXM Home Assistant Integration

This is a custom integration for [Home Assistant](https://www.home-assistant.io/) to connect WeatherXM devices to your smart home. The integration retrieves weather data from WeatherXM's cloud API and displays it as sensors in Home Assistant.

## Features

- **Sensor Data**: Displays multiple weather metrics like temperature, humidity, wind speed, solar irradiance, and more.
- **Device Grouping**: Groups all sensors from the same WeatherXM station into one device in Home Assistant.
- **Localized Friendly Names**: Sensors have friendly names in German for better readability.
- **Periodic Updates**: Fetches fresh data every 5 minutes from the WeatherXM API.

## Installation

### Manual Installation
1. Download this repository as a ZIP file and extract it.
2. Copy the `custom_components/weatherxm` folder to your Home Assistant configuration directory: `<config_directory>/custom_components/`.
3. Restart Home Assistant.

## Configuration

### Adding the Integration
1. In Home Assistant, navigate to **Settings > Devices & Services**.
2. Click the **Add Integration** button and search for `WeatherXM`.
3. Enter the required API details:
   - **Index**: The WeatherXM cell index.
   - **Device ID**: Your WeatherXM device's unique identifier.
4. Click **Submit**.

### Sensors Created
The integration will create the following sensors (localized to German):

| Sensor Type               | Friendly Name            | Unit                |
|---------------------------|--------------------------|---------------------|
| `temperature`             | Temperatur              | °C                 |
| `humidity`                | Luftfeuchtigkeit        | %                  |
| `wind_speed`              | Windgeschwindigkeit     | m/s                |
| `wind_gust`               | Windböen                | m/s                |
| `wind_direction`          | Windrichtung            | °                  |
| `solar_irradiance`        | Sonnenstrahlung         | W/m²               |
| `uv_index`                | UV-Index               | -                  |
| `precipitation`           | Niederschlag            | mm/h               |
| `precipitation_accumulated` | Niederschlagsmenge    | mm                 |
| `pressure`                | Luftdruck               | hPa                |
| `dew_point`               | Taupunkt                | °C                 |
| `feels_like`              | Gefühlte Temperatur     | °C                 |

## Known Issues

- The integration requires a stable internet connection to access the WeatherXM API.
- Ensure your WeatherXM device is registered and active in the WeatherXM system.

## Development

### Requirements
- Python 3.12+
- Home Assistant Core development environment

### Testing
1. Clone this repository to your development environment.
2. Use Home Assistant's development tools to test and debug the integration.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
