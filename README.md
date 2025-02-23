# Grafana Docker Implementation

## FRAMEWORK
Below is the technical specifications of the Grafana App
- Grafana (grafana:latest)
- InfluxDB (influxdb:2.7)
  
## LOCAL INSTALLATION

### Docker Usage

Run the command below to start-up Docker deployment:
```
docker compose up --build
```
Once done, open a browser of your choice and type in the following:

To open Granana:

```
localhost:3000
```

To open InfluxDB:

```
localhost:8086
```

## Grafana User Interface Modifications

### Titles

Open the file `Dockerfile` and update the contents on your specified titles and text modifications.

Once done, rebuild the application using the command:

```
docker compose up --build
```
### Images

Locate the `img` folder and modify the following files:

* fav32.png
* grafana_icon.svg

> **Note:** Be sure to retain the filenames or else you would need to update the contents in the file `Dockerfile`

Once done, rebuild the application using the command:

```
docker compose up --build
```

## Credentials

Locate the file `docker-compose.yml` to check the admin credentials used by Grafana and InfluxDB instances. You may update these in the file and rebuild the applcation using this command:

```
docker compose up --build
```

> **Note:**: Make sure to have these accesses modified in the web application.

## Deployment

This section only discusses the deployment guide for Amazon Web Services (AWS). It is already understood that you have created your AWS instance already. For this guide, it is assumed that you are using Amazon Linux type.

Requirements:
* Git
* Docker
* nginx

### Installations

#### Git

Install Git into the machine:

```
sudo yum update
sudo yum install git -y
```

Update credentials:

```
git config --global user.name "your_username"
git config --global user.email "your_email"
```

Clone the repository:

```
git clone https://github.com/GeoSED/grafana-docker.git
```

#### Docker

Install Docker into the machine:

```
sudo yum install docker -y 
sudo systemctl start docker
sudo systemctl enable docker
```

Install docker-compose into the machine:

```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.30.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
ls -lh /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Verify successful installation by checking the version:

```
docker-compose --version
```

#### Nginx

Install nginx into the machine:

```
sudo yum install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

Create Grafana configuration:

```
sudo nano /etc/nginx/conf.d/grafana.conf
```

Copy the contents into the newly created `grafana.conf`:

```
server {
    server_name enter-your-ec2-dnsnamehere;
    listen 80;
    access_log /var/log/nginx/grafana.log;

    # Increase buffer sizes
    proxy_buffers 8 16k;
    proxy_buffer_size 32k;
    proxy_max_temp_file_size 0;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-Host $host:$server_port;
        proxy_set_header X-Forwarded-Server $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /influxdb/ {
        proxy_pass http://localhost:8086;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-Host $host:$server_port;
        proxy_set_header X-Forwarded-Server $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

> **Note**: Make sure to update `enter-your-ec2-dnsnamehere` into your DNS

Verify if the configuration modified is working:

```
sudo nginx -t
```

In case it fails, open the `nginx.conf` and add this configuration `server_names_hash_bucket_size to 128;`

```
sudo nano /etc/nginx/nginx.conf
```

Restart the nginx instance after a successful configuration:

```
sudo systemctl restart nginx
```

### Usage

Run the command below to start-up Docker deployment:
```
docker compose up --build
```
Once done, open a browser of your choice and type in the following:

To open Granana:

```
http://your_server_dns/
```

or

```
http://your_server_ip:3000
```

To open InfluxDB:

```
http://your_server/dns/influxdb/
```

or 

```
http://your_server_ip:8086
```