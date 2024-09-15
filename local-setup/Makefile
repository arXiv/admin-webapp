
default: /usr/sbin/nginx /etc/nginx/sites-enabled/admin-console /var/www/html/arxiv

/usr/sbin/nginx:
	sudo apt install -y nginx
	sudo install -m 644 nginx/nginx.conf /etc/nginx/nginx.conf

/var/log/nginx/admin-console/:
	sudo mkdir -p /var/log/nginx/admin-console/
	sudo chown www-data:adm /var/log/nginx/admin-console/

/etc/nginx/sites-enabled/admin-console: /var/log/nginx/admin-console/
	-sudo ln -s ${HOME}/arxiv/admin-webapp/local-setup/nginx/admin-console /etc/nginx/sites-enabled/admin-console
	sudo systemctl restart nginx

/var/www/html/arxiv:
	sudo rsync -av --delete ${HOME}/arxiv/admin-webapp/local-setup/htdoc/arxiv/ /var/www/html/arxiv/
