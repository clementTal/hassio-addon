FROM raspbian/stretch

# Copy data
COPY run-ssh.sh /

RUN apt update \
    && apt-get install -y apt-utils apt-transport-https jq unzip openssh-server \
    && mkdir -p /var/run/sshd \
    && mkdir /etc/ssh/ \
    && chmod a+x /var/run/sshd \
    && chmod a+x /run-ssh.sh \
    && chmod a+x /etc/ssh/ \
 

ADD sshd_config /etc/ssh/sshd_config

EXPOSE 22

ENTRYPOINT [ "/run-ssh.sh" ]
