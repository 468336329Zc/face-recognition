chown -R mysql:mysql /var/lib/mysql /var/run/mysqld 
service mysql restart
python3 /app/face_web/run.py
