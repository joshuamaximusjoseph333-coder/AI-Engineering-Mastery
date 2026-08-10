# Day 4 — Docker and Containerization

## What I Worked On

Today I containerized Project 01 using Docker. I learned how Docker images and containers work, created a Dockerfile and `.dockerignore`, built my own project image, ran the application inside a Linux container, and verified that the pytest test suite also works inside Docker.

---

## 1. Docker Fundamentals

I learned the relationship between a Dockerfile, image, and container:

```text
Dockerfile
    ↓
docker build
    ↓
Docker Image
    ↓
docker run
    ↓
Container
```

* **Dockerfile** — instructions Docker uses to build an image.
* **Docker image** — a packaged, reusable template containing the environment, dependencies, and application files.
* **Docker container** — a running instance created from an image.

I also learned that the Docker CLI and Docker Engine are different.

* The **Docker CLI** accepts commands such as `docker build` and `docker run`.
* The **Docker Engine** performs the actual Docker operations.

---

## 2. First Linux Container

I tested Docker using the Alpine Linux image:

```bash
docker run --rm alpine uname -a
```

Docker did not initially have the Alpine image locally, so it pulled the image and created a temporary container from it.

`uname -a` displayed information about the Linux system/kernel being used.

The `--rm` option automatically removed the container after its command finished, while the reusable Alpine image remained locally.

I verified this using:

```bash
docker images
docker ps -a
```

This helped me understand that an image and a container are not the same thing.

---

## 3. Creating the Project Dockerfile

I created a `Dockerfile` in Project 01:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### `FROM python:3.13-slim`

Uses a lightweight Python 3.13 image as the base for the project image.

### `WORKDIR /app`

Sets `/app` as the working directory inside the Docker image. Docker creates the directory if it does not already exist.

### `COPY requirements.txt .`

Copies `requirements.txt` from the Docker build context into the current working directory inside the image.

Since the working directory is `/app`, the destination becomes:

```text
/app/requirements.txt
```

### `RUN pip install --no-cache-dir -r requirements.txt`

Installs the project's Python dependencies while the Docker image is being built.

### `COPY . .`

Copies the project files from the Docker build context into `/app` inside the image.

I learned that the two dots have different contexts:

```text
COPY     .                 .
         ↓                 ↓
build context         /app inside image
```

### `CMD ["python", "main.py"]`

Defines the default command that runs when a container starts from the image.

---

## 4. RUN vs CMD

An important distinction I learned was:

```text
RUN → executes while building the image

CMD → default command executed when a container starts
```

For example:

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

runs during `docker build`.

Whereas:

```dockerfile
CMD ["python", "main.py"]
```

is used when the container starts.

---

## 5. Docker Build Context

I learned that `.` represents the current directory in commands such as:

```bash
docker build -t engineering-workbench .
```

Because I ran the command from:

```text
C:\AI-Engineering-Mastery\Projects\Project-01-Engineering-Workbench
```

that Project 01 directory became the Docker build context.

Therefore, the first `.` in:

```dockerfile
COPY . .
```

refers to the contents available from that build context.

---

## 6. `.dockerignore`

I created a `.dockerignore` file to prevent unnecessary local files from being included in the Docker build context.

It includes entries such as:

```text
.venv/
__pycache__/
*.pyc
.pytest_cache/
.git/
.env
```

The local `.venv` should not be copied because it belongs to the local Windows development environment. The Docker image has its own Linux-based Python environment and installs the required dependencies using `requirements.txt`.

I also learned the distinction:

```text
.gitignore    → tells Git what not to track

.dockerignore → tells Docker what to exclude from the build context
```

---

## 7. Building the Project Image

I built the image using:

```bash
docker build -t engineering-workbench .
```

The resulting image was:

```text
engineering-workbench:latest
```

I verified it using:

```bash
docker images
```

---

## 8. Running Project 01 Inside Docker

I ran the application using:

```bash
docker run --rm engineering-workbench
```

The container successfully executed `python main.py`.

Output:

```text
INFO | Reading file: data/raw/orders.csv
4
```

This proved that Project 01 could run inside the Linux-based Docker environment instead of relying directly on my local Windows `.venv`.

---

## 9. Inspecting the Container Filesystem

I inspected `/app` using:

```bash
docker run --rm engineering-workbench ls -la /app
```

This showed that the project files had been copied into `/app`.

It also confirmed that `.venv` was not included because it was excluded using `.dockerignore`.

I learned that providing:

```text
ls -la /app
```

after the image name overrides the image's default `CMD` for that particular container run.

---

## 10. Running Tests Inside Docker

I ran the pytest test suite inside the container:

```bash
docker run --rm engineering-workbench python -m pytest
```

Result:

```text
4 passed
```

This confirmed that both the application and its automated tests work inside the Docker environment.

---

## 11. Docker Image Rebuild Experiment

I temporarily modified `main.py` after the Docker image had already been built.

The local version reflected the change, but running the existing Docker image still produced the old behavior.

This demonstrated that changing local source files does not automatically modify an already-built Docker image.

To include the updated code, I had to rebuild:

```bash
docker build -t engineering-workbench .
```

After rebuilding, newly created containers contained the updated project code.

I then removed the temporary change and rebuilt the final image again.

---

## Key Concepts Learned

* Dockerfile vs image vs container
* Docker CLI vs Docker Engine
* Pulling an existing image vs building my own image
* Linux containers on a Windows host through Docker Desktop/WSL2
* Docker build context
* `FROM`
* `WORKDIR`
* `COPY`
* `RUN`
* `CMD`
* `RUN` vs `CMD`
* `.dockerignore`
* `--rm`
* Overriding the default `CMD`
* Running pytest inside Docker
* Rebuilding images after source-code changes
* Using Docker to create a consistent and reproducible runtime environment

---

## Day 4 Result

By the end of Day 4, Project 01 could be:

1. Run locally using the Python virtual environment.
2. Tested locally using pytest.
3. Built as a Docker image.
4. Run inside a Linux-based Docker container.
5. Tested inside the Docker container.

This moved the project from a locally working Python application toward a more portable and reproducible engineering workflow.
