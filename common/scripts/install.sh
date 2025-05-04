#!/bin/bash
sudo dnf install -y fontconfig graphviz git-subtree java-24-amazon-corretto
export PLANTUML_VERSION="1.2025.2"
wget "https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar"
mv "plantuml-${PLANTUML_VERSION}.jar" ./scripts/plantuml.jar
