# rubbish-day

## Clone to local machine

```
git clone https://
```

## Running with `docker`

Unsurprisingly, you'll need [Docker](https://www.docker.com/products/docker-desktop) 
installed to run this project with Docker. To build a containerised version of the API, 
run:

```bash
docker build . -t flask-app
```

To launch the containerised app, run:

```bash
docker run -p 5000:5000 flask-app
```

You should see your server boot up, and should be accessible as before.

## Developing with the template

To develop the template for your own project, you'll need to make sure to [create your
own repository from this template](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template) 
and then install the project's development dependencies. You can do this with:

```bash
pip install -r requirements/develop.txt
```

This'll install some style formatting and testing tools (including `pytest` and 
`locust`).
