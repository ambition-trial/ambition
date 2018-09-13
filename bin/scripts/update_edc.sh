migrate=""
update_permissions=""
update_ubuntu=""
green=`tput setaf 2`
reset=`tput sgr0`

while true; do
    read -p "Update this script? [y/n]" yn
    case $yn in
        [Yy]* ) update_script="y"; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

if [ "${update_script}" = "y" ]; then
  echo "${green}Copying script ... ${reset}" 
  cd ~/app \
  && git checkout master \
  && git pull \
  && cp bin/scripts/update_edc.sh ~/
  echo "${green}Done ... ${reset}"
  exit
fi

while true; do
    read -p "Update repo and env? [y/n]" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
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
    read -p "Update edc permissions? [y/n]" yn
    case $yn in
        [Yy]* ) update_permissions="y"; break;;
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
echo "${green}Start ... ${reset}"

cd ~/app \
  && git checkout master \
  && git pull \
  && version=$(head -n 1 VERSION) \
  && echo "Version ${version}"

cd ~/app \
  && git checkout master \
  && git pull \
  && . ~/.venvs/ambition/bin/activate \
  && pip install --no-cache-dir -U -r requirements/stable-v${version}.txt \
  && pip install -e .

if [ "${migrate}" = "y" ]; then
  echo "${green}Running migrations ... ${reset}"
  cd ~/app \
  && python manage.py migrate
fi

 if [ "${update_permissions}" = "y" ]; then
  echo "${green}Updating permissions ... ${reset}"
  cd ~/app \
  && python manage.py update_edc_permissions
fi

if [ "${update_ubuntu}" = "y" ]; then
  echo "${green}Updating permissions ... ${reset}"
  sudo apt-get update \
  && sudo apt-get upgrade
fi

echo "${green}Restarting gunicorn / gunicorn-uat ... ${reset}"
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart gunicorn-uat

echo "${green}Done.${reset}"
