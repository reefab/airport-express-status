# Airport Express Status

Trivial Python Rest API server that does one thing: give it the hostname/ip of a airport express and it'll tell you if it's currently receiving an Airplay stream.

No external dependencies.

## Usage

```shell
docker run -p 8000:8000 reefab/airport-express-status:latest
```

```shell
curl localhost:8000/airport.home.arpa
```

```json
{"Status": true}
```

## Home Assistant

Create a binary_sensor.

```yaml
binary_sensor:
  - platform: rest
    name: Airport Express Airplay Status
    resource: http://localhost:8000/airport.home.arpa
    scan_interval: 5
    value_template: "{{ value_json.Status }}"
```

Use it in an automation:

```yaml
  - alias: 🔈 Switch on receiver if airplay is active
    trigger:
      platform: state
      entity_id: binary_sensor.airport_express_airplay_status
      to: 'on'
    action:
      - service: media_player.turn_on
        entity_id: media_player.yamaha_receiver
      - service: media_player.select_source
        entity_id: media_player.yamaha_receiver
        data:
          source: 'AV4'
```
