CONFIG_PATH=/data/options.json

SSH_ENABLED=$(jq --raw-output '.ssh.enabled' $CONFIG_PATH)
SSH_LOGIN=$(jq --raw-output '.ssh.login' $CONFIG_PATH)
SSH_PASSWORD=$(jq --raw-output '.ssh.password' $CONFIG_PATH)


echo "==================================="
echo "----------- CONFIG SSH ------------"
echo "==================================="

echo "SSH config: $SSH_LOGIN:$SSH_PASSWORD"
echo "$SSH_LOGIN:$SSH_PASSWORD" | chpasswd

/usr/sbin/sshd -D -ddd -e
