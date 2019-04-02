FROM raspbian/stretch


# Copy data
COPY run-ssh.sh /
RUN apt upgrade && apt-get install -y apt-utils apt-transport-https jq unzip openssh-server

RUN mkdir -p /var/run/sshd \
    && chmod a+x /var/run/sshd \
    && chmod a+x /run-ssh.sh

ADD sshd_config /etc/ssh/sshd_config

EXPOSE 22

ENTRYPOINT [ "/run-ssh.sh" ]
