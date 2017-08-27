############################################################
# Dockerfile to build scrapyd container images
# Based on Python:3 image
############################################################
FROM python:3

MAINTAINER jcfg

# Install scrapyd
RUN pip install scrapyd

# Expose port for inter-container comms
EXPOSE 6800

# Copy the configuration file
COPY scrapyd.conf /etc/scrapyd/

# Volume for the output of the scrapyd stuff
VOLUME /var/lib/scrapyd

# Launch the daemon upon starting
CMD ["scrapyd"]
