# GPT Teacher DB

Models, migrations and everything related to GPT Teacher's databases


# Installation

Install the package in your environment **using pip** by running the command:

```console
pip install git+ssh://git@github.com/your-org/gpt-teacher-db.git
```

ou

```console
pip install git+https://<TOKEN>@github.com/your-org/gpt-teacher-db.git
```

> Or even add this to a new line in your `requirements.txt` file: `git+ssh://git@github.com/your-org/gpt-teacher-db.git`


<!-- # Migrations -->

<!-- Adicione explicação da necessidade de adicionar isso nos modelos:

from sqlalchemy.sql import false
sa_column_kwargs={'server_default': false()}
-->


# Environment

To set up a Python environment to run migrations on the DB or develop the **`gpt_teacher_db`** package, run the commands:

(*Optional*) Set the Python version to be used, in case there's more than one installed:

```console
uv venv
```

Activate the environment

```console
source .venv/bin/activate
```

Install the dependencies

```console
uv sync
```

# Sample run code
> Sample run
> ```bash
> make migrations name='Test migration' schema=gpt_teacher
```