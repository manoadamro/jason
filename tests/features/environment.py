import docker


def before_all(context):
    context.docker = docker.from_env()
    context.containers = {}


def after_all(context):
    for name, container in context.containers.items():
        container.stop()
        container.remove()
