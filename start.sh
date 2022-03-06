#!/bin/bash

cd tasks;

for d in */ ; do
    if [ -f "./$d/task/docker-compose.yml" ];then
        cd "$d/task";
        docker-compose up --force-recreate --build -d;
        cd ../.. ;
    fi
done

cd ..;
