# rubbish-day

`rubbish-day` is a container that runs a single python script that scrapes the Auckland Council website for data about your rubbish collection service. This data can then be consumed by Home Assistant.

Your `AddressID` is found at the end of the URL when you search your address at the [Auckland Council Website](https://www.aucklandcouncil.govt.nz/rubbish-recycling/rubbish-recycling-collections/Pages/rubbish-recycling-collection-days.aspx)



## Running with `docker`

Unsurprisingly, you'll need [Docker](https://www.docker.com) installed to run this project with Docker. 

To launch the container, run:

```bash
docker run -d --name rubbish-day -e TZ=Pacific/Auckland -p 5050:5050 --restart unless-stopped ghcr.io/reubznz/rubbish-day
```


## Adding to `Home Assistant`

In [Home Assistant](https://www.home-assistant.io/), launch `Studio Code Server` and open `sensors.yaml` if you have it separated, or `configuration.yaml`.

Add the following, customising the resource address and appending your Address ID:

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
    - data_retrieved_datetime
  scan_interval:
    hours: 1
```

Restart Home Assistant to load the new sensor. Updates to the sensor configuration should be able to be done by performing a quick reload in the new `Home Assistant` restart window.



## Build from source

Clone to local machine

```
git clone https://github.com/reubznz/rubbish-day.git
```

To manually build the container, run:

```
docker build . -t rubbish-day
```

To launch the container, run:

```
docker run -d --name rubbish-day -e TZ=Pacific/Auckland -p 5050:5050 --restart unless-stopped rubbish-day
```


## Thanks to

[jeremysherriff](https://github.com/jeremysherriff) for building the core Python script

https://mark.douthwaite.io/getting-production-ready-a-minimal-flask-app/ & https://github.com/markdouthwaite/minimal-flask-api/tree/main/requirements for providing a simple to use template for creating a docker image
