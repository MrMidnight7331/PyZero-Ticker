python3 ./changecfg.py
if [ $? -eq 0 ]; then
  sudo systemctl restart btc-screen.service
fi
