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
docker run -d --name rubbish-day -p 5055:5055 --restart unless-stopped rubbish-day
```
