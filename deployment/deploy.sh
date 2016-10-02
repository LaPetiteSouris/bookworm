#!/usr/bin/env bash


# Trigger Docker image build

BUILD_TRIGGER='https://registry.hub.docker.com/u/souris/bookworm/trigger/02675d92-7ad1-4b99-982b-cd7faa86bf03/
'

IMAGE='souris/bookworm'

build_image(){
    printf 'Triggering Docker Image build on Docker hub. Notice that only pushed commit will be built \n'
    curl -X POST ${BUILD_TRIGGER}

    #TODO: Docker Build completion check should be automatic
    printf '\n Please wait for the build complete before executing anything else'
}

main()
{
    build_image

    printf '\n Please make sure the build is completed on Docker Hub'
    read -r -p "Is it completed ? [y/N] " response
    if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
    then
        ssh $1 'bash -s' < './setup_remote_docker.sh'
    fi
}

main "$@"