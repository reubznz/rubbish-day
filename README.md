# rubbish-day

`rubbish-day` is a container that runs a single python script that scrapes the Auckland Council website for data about your rubbish collection service. This data can then be consumed by Home Assistant.


## Clone to local machine

```
git clone https://github.com/reubznz/rubbish-day.git
```


## Running with `docker`

Unsurprisingly, you'll need [Docker](https://www.docker.com) 
installed to run this project with Docker. To build the container, 
run:

```bash
docker build . -t rubbish-day
```

To launch the container, run:

```bash
docker run -d --name rubbish-day -p 5050:5050 --restart unless-stopped rubbish-day
```


## Adding to `Home Assistant`

In [Home Assistant](https://www.home-assistant.io/), launch `Studio Code Server` and open `sensors.yaml` if you have it separated, or `configuration.yaml`.

Add the following, customising the resource address:

```
- platform: rest
  name: Rubbish Day
  resource: http://ip.add.re.ss:5050/rubbish-day?addressid=12345678910
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

## Thanks to

https://mark.douthwaite.io/getting-production-ready-a-minimal-flask-app/ & https://github.com/markdouthwaite/minimal-flask-api/tree/main/requirements
