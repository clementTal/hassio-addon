CONFIG_PATH=/data/options.json

SSH_ENABLED=$(jq --raw-output '.ssh.enabled' $CONFIG_PATH)
SSH_LOGIN=$(jq --raw-output '.ssh.login' $CONFIG_PATH)
SSH_PASSWORD=$(jq --raw-output '.ssh.password' $CONFIG_PATH)

SUPERVISORD_CONF_FILE="/etc/supervisor/conf.d/supervisord.conf"

echo "==================================="
echo "----------- CONFIG SSH ------------"
echo "==================================="

echo "SSH config: $SSH_LOGIN:$SSH_PASSWORD"
echo "$SSH_LOGIN:$SSH_PASSWORD" | chpasswd

# SSH login fix. Otherwise user is kicked off after login
sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

echo "export VISIBLE=now" >> /etc/profile

# Generate global configuration
cat <<EOT > $SUPERVISORD_CONF_FILE
[supervisord]
nodaemon=true

[inet_http_server]
port      = :9001
username  = elao
password  = boumbo

EOT

if [ "${SSH_ENABLED}" = true ]
then
    cat <<EOT >> $SUPERVISORD_CONF_FILE
[program:sshd]
command=/usr/sbin/sshd -D -ddd -e
autostart=true
autorestart=true
startretries=20

EOT
else
    echo "SSH is disabled"
fi