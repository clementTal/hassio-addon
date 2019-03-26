ARG BUILD_FROM
FROM $BUILD_FROM

# Copy data
COPY run.sh /
COPY mosquitto.conf /etc/
COPY customtts.sh /usr/bin
COPY snips-entrypoint.sh /
COPY run-ssh.sh /

ARG BUILD_ARCH


RUN apt update 
RUN apt-get install -y dirmngr apt-utils apt-transport-https jq unzip supervisor mpg123 curl tzdata python-pip git openssh-server supervisor

RUN rm -rf /var/lib/apt/lists/*
RUN if [ "$BUILD_ARCH" = "amd64" ]; then bash -c 'echo "deb https://debian.snips.ai/stretch stable main" > /etc/apt/sources.list.d/snips.list' \
        && apt-key adv --keyserver pgp.surfnet.nl --recv-keys F727C778CCB0A455; \
    else bash -c 'echo "deb https://raspbian.snips.ai/stretch stable main" > /etc/apt/sources.list.d/snips.list' \
        && apt-key adv --keyserver pgp.surfnet.nl --recv-keys D4F50CDCA10A2849; \
    fi

RUN apt-get update
RUN apt-get install -y snips-platform-voice snips-skill-server snips-analytics snips-asr snips-audio-server snips-dialogue snips-hotword snips-nlu snips-tts snips-watch snips-template  
RUN rm -rf /var/lib/apt/lists/* 
RUN chmod a+x /run.sh 
RUN chmod a+x /usr/bin/customtts.sh 
RUN chmod a+x /snips-entrypoint.sh 
RUN chmod a+x /run-ssh.sh 

RUN curl -L -o /assistant_Hass_de.zip https://s3.amazonaws.com/hassio-addons-data/assistant_Hass_de.zip 
RUN curl -L -o /assistant_Hass_en.zip https://s3.amazonaws.com/hassio-addons-data/assistant_Hass_en.zip 
RUN curl -L -o /assistant_Hass_fr.zip https://s3.amazonaws.com/hassio-addons-data/assistant_Hass_fr.zip

ENV NOTVISIBLE "in users profile"

EXPOSE 22

ENTRYPOINT [ "/run.sh" ]
