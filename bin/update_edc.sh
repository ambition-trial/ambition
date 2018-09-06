migrate=""
update_permissions=""
update_ubuntu=""
green=`tput setaf 2`
reset=`tput sgr0`

while true; do
    read -p "Update repo and env? [y/n]" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
while true; do
    read -p "Update edc permissions? [y/n]" yn
    case $yn in
        [Yy]* ) update_permissions="y"; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done
while true; do
    read -p "Run migrations? [y/n]" yn
    case $yn in
        [Yy]* ) migrate="y"; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done
while true; do
    read -p "Update UBUNTU? [y/n]" yn
    case $yn in
        [Yy]* ) update_ubuntu="y"; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done
echo "${green}Updating ENV ... ${reset}"

if [ "${update_ubuntu}" = "y" ]; then
  echo "${green}Updating permissions ... ${reset}"
  sudo apt-get update \
  && sudo apt-get upgrade
fi

cd ~/app \
  && git pull \
  && . ~/.venvs/ambition/bin/activate \
  && pip install --no-cache-dir -U -r requirements/stable.txt \
  && pip install -e .

 if [ "${update_permissions}" = "y" ]; then
  echo "${green}Updating permissions ... ${reset}"
  cd ~/app \
  && python manage.py update_edc_permissions
fi
if [ "${migrate}" = "y" ]; then
  echo "${green}Running migrations ... ${reset}"
  cd ~/app \
  && python manage.py migrate
fi

echo "${green}Restarting gunicorn / gunicorn-uat ... ${reset}"
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart gunicorn-uat

echo "${green}Done.${reset}"
