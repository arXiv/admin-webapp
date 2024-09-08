
default: /etc/nginx/sites-enabled/admin-console

/var/log/nginx/admin-console/:
	sudo mkdir -p /var/log/nginx/admin-console/
	sudo chown www-data:adm /var/log/nginx/admin-console/

/etc/nginx/sites-enabled/admin-console: /var/log/nginx/admin-console/
	-sudo ln -s ${HOME}/arxiv/admin-webapp/local-setup/nginx/admin-console /etc/nginx/sites-enabled/admin-console
	sudo systemctl restart nginx
