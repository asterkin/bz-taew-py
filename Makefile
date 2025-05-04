PUML_DIR = ./docs/puml
DIAGRAMS_DIR = ./docs/diagrams

# List of .puml files in the docs/puml directory
PUML_FILES = $(wildcard $(PUML_DIR)/*.puml)

# Corresponding .png files in the docs/diagrams directory
DIAGRAM_FILES = $(patsubst $(PUML_DIR)/%.puml, $(DIAGRAMS_DIR)/%.png, $(PUML_FILES))

# Rule to build all diagram files
all-diagrams: $(DIAGRAM_FILES)

# Rule to build each diagram from its corresponding puml file
# For some reason, the output should be relative to the puml file
$(DIAGRAMS_DIR)/%.png: $(PUML_DIR)/%.puml
	@echo "Generating diagram for $<..."
	@./scripts/plantuml.sh ./$< -o ../diagrams/ 