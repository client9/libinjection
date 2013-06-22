#!/bin/bash
fname=$1

echo '{% extends "base.html" %}'
echo '{% block body %}'
github-markup $fname
echo '{% end %}'
