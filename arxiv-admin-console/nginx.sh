#!/bin/sh

cat > /usr/share/nginx/html/env-config.json <<EOF
{
  "AAA_URL": "${AAA_URL}",
  "ADMIN_API_BACKEND_URL": "${ADMIN_API_BACKEND_URL}",
  "ADMIN_APP_ROOT": "${ADMIN_APP_ROOT}"
}
EOF

nginx -g 'daemon off;'
