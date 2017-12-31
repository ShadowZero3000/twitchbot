FROM python

RUN apt-get update && apt-get install -y stunnel \
 && cp /etc/ssl/openssl.cnf tmpopenssl.cnf \
 && printf '[SAN]\nsubjectAltName=DNS:music.codethat.rocks, IP:192.168.99.100' >> tmpopenssl.cnf \
 && openssl req \
      -new -x509 -days 365 -nodes -out stunnel.pem -keyout stunnel.key \
      -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=music.codethat.rocks" \
      -reqexts SAN \
      -extensions SAN \
      -config tmpopenssl.cnf \
      -sha256 \
 && mv stunnel.key stunnel.pem /etc/stunnel/ \
 && chmod 600 /etc/stunnel/stunnel.key

COPY bot /bot
WORKDIR /bot

RUN pip install --no-cache-dir -r requirements.txt
COPY stunnel.conf /etc/stunnel/stunnel.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000

CMD ["/entrypoint.sh"]

# Run with: docker run -it -v $(pwd)/bot/current_song:/bot -p 5000:443 music-queue-bot /bin/bash