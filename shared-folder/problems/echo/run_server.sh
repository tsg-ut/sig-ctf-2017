#!/bin/bash
socat TCP-L:3000,reuseaddr,fork EXEC:./echo
