apt-get update
apt-get dist-upgrade -y

apt-get install python3-pip python-opencv -y -q





pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip==9.0.1
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt

python3 /app/face_web/create_db.py

echo "done!"

