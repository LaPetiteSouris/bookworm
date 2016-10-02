#!/usr/bin/env bash

IMAGE='souris/bookworm'


deploy_docker_image()
{
    # update docker image
    docker pull ${IMAGE}

    # update container with new image
    printf 'Stop old docker container: '
    docker stop bookworm_server
    printf 'Remove old docker container: '
    docker rm bookworm_server

    # launch new service
    # TODO: Should be zero-down time here
    printf 'Launching new docker container: '
    docker run --name bookworm_server -p 0.0.0.0:3000:3000 -d souris/bookworm
}

main()
{
    deploy_docker_image
}

main