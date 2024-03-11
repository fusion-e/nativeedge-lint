# Makefile for collecting and installing requirements for nativeedge-plugins-sdk.
VENVS := $(shell pyenv virtualenvs --skip-aliases --bare | grep 'project\b')
SHELL := /bin/bash

default:
	make setup_local_virtual_env
	make run_tests

compile:
	make setup_local_virtual_env

setup_local_virtual_env:
ifneq ($(VENVS),)
	@echo We have $(VENVS)
	pyenv virtualenv-delete -f project && pyenv deactivate
endif
	pyenv virtualenv 3.11 project

cleanup:
	pyenv virtualenv-delete -f project

run_tests:
	@echo "Starting executing the tests."
	HOME=${HOME} VIRTUAL_ENV=${HOME}/.pyenv/${VENVS} tox

clrf:
	@find . \( -path ./.tox -prune -o -path ./.git -prune \) -o -type f -exec dos2unix {} \;

prune:
	@find . -name "*.pyc" -exec rm -f {} \;
