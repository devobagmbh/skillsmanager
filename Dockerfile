FROM python:3-alpine

RUN adduser -D -u 1000 app && mkdir /app && chown app /app
RUN apk add gcc python3-dev musl-dev g++ glib pango

WORKDIR /app
USER 1000

COPY --chown=app . .

RUN python -m venv .venv
RUN . .venv/bin/activate && pip install -r requirements.txt
RUN . .venv/bin/activate && pip install daphne
RUN . .venv/bin/activate && SECRET_KEY=required python manage.py collectstatic --noinput

USER root
RUN chown app -R .

USER 1000

EXPOSE 8000

ENTRYPOINT [ "/bin/sh", "entrypoint.sh" ]