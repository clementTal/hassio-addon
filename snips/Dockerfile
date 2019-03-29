ARG BUILD_FROM
FROM raspbian/stretch

ENV INITRD No

# Copy data
COPY run.sh /
COPY mosquitto.conf /etc/
COPY customtts.sh /usr/bin
COPY snips-entrypoint.sh /
COPY run-ssh.sh /

RUN apt update \
    && apt-get install -y dirmngr apt-utils apt-transport-https jq unzip supervisor mpg123 curl tzdata python-pip git openssh-server

RUN rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd
RUN chmod 0755 /var/run/sshd

ADD sshd_config /etc/ssh/sshd_config

RUN mkdir -p /data /data/debian-base /data/debian-base/log


RUN bash -c 'echo "deb https://raspbian.snips.ai/stretch stable main" > /etc/apt/sources.list.d/snips.list'
RUN apt-key adv --keyserver gpg.mozilla.org --recv-keys D4F50CDCA10A2849; 


RUN apt-get update \
    && apt-get install -y snips-platform-voice snips-skill-server snips-analytics snips-asr snips-audio-server snips-dialogue snips-hotword snips-nlu snips-tts snips-watch snips-template  \
    && rm -rf /var/lib/apt/lists/* \
    && chmod a+x /run.sh \
    && chmod a+x /usr/bin/customtts.sh \
    && chmod a+x /snips-entrypoint.sh \
    && chmod a+x /run-ssh.sh \

RUN curl -L -o /assistant_Hass_de.zip https://s3.amazonaws.com/hassio-addons-data/assistant_Hass_de.zip 
RUN curl -L -o /assistant_Hass_en.zip https://s3.amazonaws.com/hassio-addons-data/assistant_Hass_en.zip 
RUN curl -L -o /assistant_Hass_fr.zip https://s3.amazonaws.com/hassio-addons-data/assistant_Hass_fr.zip

ENV NOTVISIBLE "in users profile"

EXPOSE 22

ENTRYPOINT [ "/run.sh" ]
