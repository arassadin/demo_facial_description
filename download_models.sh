echo "[$(date +"%T")] [INFO] Downloading Levi et al. age model.."
wget -nv https://dl.dropboxusercontent.com/u/38822310/age_net.caffemodel -O models/Levi\ et\ al./age_weights.caffemodel
[[ $? > 0 ]] && { echo "[ERROR] Unable to download model"; exit 1; }

echo "[$(date +"%T")] [INFO] Downloading Levi et al. gender model.."
wget -nv https://dl.dropboxusercontent.com/u/38822310/gender_net.caffemodel -O models/Levi\ et\ al./gender_weights.caffemodel
[[ $? > 0 ]] && { echo "[ERROR] Unable to download model"; exit 1; }

echo "[$(date +"%T")] [INFO] Downloading Rothe et al. age model.."
wget -nv https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/dex_chalearn_iccv2015.caffemodel -O models/Rothe\ et\ al./age_weights.caffemodel
[[ $? > 0 ]] && { echo "[ERROR] Unable to download model"; exit 1; }

echo "[$(date +"%T")] [INFO] Downloading Rothe et al. gender model.."
wget -nv https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/gender.caffemodel -O models/Rothe\ et\ al./gender_weights.caffemodel
[[ $? > 0 ]] && { echo "[ERROR] Unable to download model"; exit 1; }

echo "[$(date +"%T")] [INFO] Models successfully downloaded and stored in the 'models' subfolder"
