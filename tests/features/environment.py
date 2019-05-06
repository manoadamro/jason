import os

import docker


def before_all(context):
    username = os.environ.get("DOCKER_USER")
    password = os.environ.get("DOCKER_PASS")
    client = docker.from_env()
    if username:
        client.login(username=username, password=password)
    context.docker = client
    context.containers = {}


def after_all(context):
    for name, container in context.containers.items():
        container.stop()
        container.remove()
