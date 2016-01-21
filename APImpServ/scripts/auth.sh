#!/bin/bash

s1="user1"
s2="contrasena"

if [ "$1" == "$s1" ] && [ "$2" == "$s2" ]; then
    exit 0
else
    exit 1
fi

