# Patience
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## Introduction
Patience is a web application designed to help healthcare professionals manage their patients and
consultations on a daily basis.
General practitioners, specialists, chiropractors, psychologists and other healthcare professionals
and alternative practitioners will be able to facilitate their patient management by centralizing
multiple functionalities such as patient diaries, calendar and slot blocking, consultation histories
and even suggestions of relevant drugs (subject to prescription authorization) available from Vidal.

## Installation
This project uses uv. The `pyproject.toml` lists all dependencies of the project.

uv:
```bash
uv venv
uv sync
```

pip:
```bash
python -m venv .venv
.venv\Scripts\activate  # windows
source .venv\Scripts\activate  # linux
python -m pip install .
```

## Launch
uv:

`uv run manage.py runserver`

others:

`python manage.py runserver`