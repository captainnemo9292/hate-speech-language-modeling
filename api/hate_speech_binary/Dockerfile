FROM continuumio/miniconda3

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . .
RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "hate_env", "/bin/bash", "-c"]

# Make sure the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

ENTRYPOINT ["conda", "run", "-n", "hate_env", "python", "app.py"]
