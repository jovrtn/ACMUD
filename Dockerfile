FROM evennia/evennia:latest
# USER 501:20
RUN pip install rich
# ENTRYPOINT evennia start -l