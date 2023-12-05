echo "Installing python 3.11"

sudo apt install python3.11

echo "Installing pip 3.11"
sudo apt install python3-pip


#source ~/.
echo "Installing git.."
sudo apt install git
echo "git successfully installed"

## install the project
echo "Installing the analytics project.."
mkdir ~/repos/
cd ~/repos/
git clone git@github.com:strategydata/houseuk-dashboard.git
cd houseuk-dashboard
echo "houseuk-dashboard repo successfully installed"

## install visual studio code
echo "Installing VS Code.."
cd ~/Downloads
curl "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64" >> vscode.deb
sudo apt install vscode.deb
code --version
rm -rf vscode.deb
echo "VS Code successfully installed"

echo "Setting up your computer to contribute to the handbook..."
cd ~/repos/
git clone git@github.com:strategydata/amberdata-link.git
echo "Handbook project successfully installed"


## create global gitignore
echo "Creating a global gitignore.."

## install the dbt

## Add in K9s installtion 
echo "Installing k9s .."
sudo apt update
sudo apt install snapd
sudo snap install k9s



echo "Onboarding script ran successfully"



