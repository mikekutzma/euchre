# Networking Setup

## Generate certificates

```bash
sudo systemctl stop nginx.service
sudo certbot certonly --standalone -d euchre.kutz.dev -d api.euchre.kutz.dev
sudo systemctl start nginx.service
```

## Link local site definition

```bash
ln -s ~/euchre/nginx/euchre.kutz.dev /home/pi/nginx/sites-enabled/
sudo systemctl restart nginx.service
```
