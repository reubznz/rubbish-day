# rubbish-day

## Clone to local machine

```
git clone https://github.com/reubznz/rubbish-day.git
```

## Running with `docker`

Unsurprisingly, you'll need [Docker](https://www.docker.com/products/docker-desktop) 
installed to run this project with Docker. To build a containerised version of the API, 
run:

```bash
docker build . -t rubbish-day
```

To launch the containerised app, run:

```bash
docker run -d --name rubbish-day -p 5050:5050 --restart unless-stopped rubbish-day
```

## Adding to `Home Assistant`

Open `configuration.yaml`

```
- platform: rest
  name: Rubbish Day
  resource: http://ip.add.re.ss:5050/?addressid=12345678910
  value_template: "{{ value_json.value }}"
  json_attributes:
    - address
    - datetime
    - collection_type
    - icon
    - next_collection_type
    - next_collection_date
    - next_collection_datetime
    - next_collection_icon
  scan_interval:
    hours: 1
```

Restart Home Assistant to load the new sensor. Updates to the sensor configuration can then be done by reloading REST yaml.
