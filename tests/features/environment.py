import os

import docker


def before_all(context):
    context.is_circle = os.environ.get("CI", None) is not None
    client = docker.from_env()
    if context.is_circle:
        username = os.environ.get("DOCKER_USER")
        password = os.environ.get("DOCKER_PASS")
        client.login(username=username, password=password)
    context.docker = client
    context.containers = {}


def after_all(context):
    for name, container in context.containers.items():
        container.stop()
        container.remove()
