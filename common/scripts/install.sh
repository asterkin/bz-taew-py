sudo sudo dnf install -y fontconfig graphviz git-subtree
wget https://corretto.aws/downloads/latest/amazon-corretto-24-aarch64-linux-jdk.rpm
sudo dnf localinstall -y amazon-corretto-24-aarch64-linux-jdk.rpm
rm amazon-corretto-24-aarch64-linux-jdk.rpm
export PLANTUML_VERSION="1.2025.2"
wget "https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar"
mv "plantuml-${PLANTUML_VERSION}.jar" ./scripts/plantuml.jar


