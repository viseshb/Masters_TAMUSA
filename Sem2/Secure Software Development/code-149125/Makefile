.DEFAULT_GOAL=help
.PHONY: run build clean help
SRC = src
BUILD = build
OBJS = $(patsubst $(SRC)/%.c, $(BUILD)/%.o, $(wildcard $(SRC)/*.c))
CFLAGS = -I $(SRC)/include
LDFLAGS =
CC = gcc
TARGET = $(BUILD)/heap_overflow_cplx-bad


run: $(TARGET) ## Run the test case

build: $(TARGET) ## Build the test case

$(TARGET): $(OBJS) ## Build the binary
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

$(BUILD)/%.o: $(SRC)/%.c ## Build object files
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< $(LDFLAGS) -o $@

clean: ## Clean the test case
	rm -r $(BUILD)

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
