ARG BUILD_FROM
FROM homeassistant/armhf-base-raspbian:stretch

# Copy data
COPY run.sh /
COPY mosquitto.conf /etc/
COPY customtts.sh /usr/bin
COPY snips-entrypoint.sh /

RUN apt-get update
RUN apt-get install -y dirmngr apt-utils apt-transport-https jq unzip supervisor mpg123 curl tzdata
RUN rm -rf /var/lib/apt/lists/*
RUN bash -c 'echo "deb https://raspbian.snips.ai/stretch stable main" > /etc/apt/sources.list.d/snips.list'
RUN apt-key adv --keyserver pgp.surfnet.nl --recv-keys D4F50CDCA10A2849;

RUN apt-get update
RUN apt-get install -y openssh-server supervisor
RUN apt-get install -y snips-platform-voice snips-skill-server mosquitto snips-analytics snips-asr snips-audio-server snips-dialogue snips-hotword snips-nlu snips-tts curl unzip snips-template python-pip git 
RUN rm -rf /var/lib/apt/lists/* 
RUN curl -L -o /assistant_Hass_de.zip https://s3.amazonaws.com/hassio-addons-data/assistant_Hass_de.zip 
RUN curl -L -o /assistant_Hass_en.zip https://s3.amazonaws.com/hassio-addons-data/assistant_Hass_en.zip 
RUN curl -L -o /assistant_Hass_fr.zip https://s3.amazonaws.com/hassio-addons-data/assistant_Hass_fr.zip

ENV NOTVISIBLE "in users profile"

EXPOSE 22

ENTRYPOINT [ "/run.sh" ]
