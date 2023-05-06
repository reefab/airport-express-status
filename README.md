# Airport Express Status

Trivial Python Rest API server that does one thing: give it the hostname/ip of a airport express and it'll tell you if it's currently receiving an Airplay stream.

No external dependencies.

## Why does this even exists

I needed a way to find out if my Airport Express was receiving Airplay so I could automatically turn on my receiver and switch to its toslink input.

The Airport Express do have a HTTP API but it speaks [Plist](https://en.wikipedia.org/wiki/Property_list), a binary format that's not readily readable for most software.

Hence this little piece of server that requests the status of the Airport Express, extracts and decode the Airplay status and reports it back in JSON.

## Usage

### Home Assistant OS
Add repository and install.

### Docker

```shell
$ docker build . --build-arg BUILD_FROM=alpine --no-cache --tag airport-express-status
```

```shell
$ docker run -p 8000:8000 airport-express-status python3 ./api.py
```

```shell
$ curl localhost:8000/<airport express hostname or IP>
```

```json
{"Status": true, "StatusCode": 200}
```

## Home Assistant

Create a binary sensor.

```yaml
binary_sensor:
  - platform: rest
    name: Airport Express Airplay Status
    resource: http://localhost:8000/airport.home.arpa # or http://airport-express-status:8000/airport.home.arpa  for home assistant OS
    scan_interval: 30
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
