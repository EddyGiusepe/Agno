// Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

/*
Client_golang.go
================
Client Go that consumes the REST API of the Agno Python server through HTTP.
Implements an interactive CLI interface with support for two response modes:
streaming in real time and complete response (without streaming).

MAIN FEATURES
---------------
✓ Interactive CLI interface for communication with the agent
✓ Two response modes:
  - Streaming (/chat/stream) - Gradual response in real time
  - Complete (/chat) - Complete response (JSON structured)

✓ Automatic health check of the Python server
✓ Colored formatting of the output using the utils package
✓ Serialization/deserialization JSON for requests and responses

USED TECHNOLOGIES
------------
• Go (net/http, encoding/json, bufio)
• FastAPI + Agno Framework (backend Python)
• HTTP REST API with streaming and JSON

RUN
---

 1. Start the Python server:
    uvicorn server_agno:app --reload --port 8000

 2. Execute the Go client:
    go run client_golang.go

 3. Choose the mode (1=Streaming, 2=Complete)

FORMATTING THE CODE
-------------------
gofmt -w client_golang.go

You can use the command <go mod tidy> to clean and reorganize your
dependencies.
*/
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"16_Agno_and_GO/api"
	"16_Agno_and_GO/utils"
)

func printHeader() {
	fmt.Println()
	fmt.Println(utils.Blue + utils.Reset + " 🤖 " + utils.Green + "AnimeBot" + utils.Reset + " - Intelligent Agent " + utils.Blue + utils.Reset)
	fmt.Println(utils.Blue + utils.Reset + " 📺 Anime + 🧠 General Knowledge " + utils.Blue + utils.Reset)
	fmt.Println()
	fmt.Println(utils.Yellow + "Type 'quit' or 'exit' to exit." + utils.Reset)
	fmt.Println(strings.Repeat("-", 35))
}

func main() {
	printHeader()

	// Check if the Python server is running
	if !api.CheckServerHealth() {
		fmt.Println(utils.Red + "❌ Agno server is not running!" + utils.Reset)
		fmt.Println(utils.Yellow + "First execute: uvicorn server_agno:app --reload --port 8000" + utils.Reset)
		return
	}
	fmt.Println(utils.Green + "✅ Agno server connected!" + utils.Reset)
	fmt.Println(strings.Repeat("-", 30))

	// Ask the user which mode to use:
	fmt.Println()
	fmt.Println(utils.Cyan + "Choose the response mode:" + utils.Reset)
	fmt.Println("  1. " + utils.Green + "Streaming" + utils.Reset + " - Gradual response in real time")
	fmt.Println("  2. " + utils.Blue + "Complete (without streaming)" + utils.Reset + " - Complete response (once)")
	fmt.Print(utils.Yellow + "Type 1 or 2 (default: 1): " + utils.Reset)

	scanner := bufio.NewScanner(os.Stdin)
	var useStreaming bool = true // default: streaming

	if scanner.Scan() {
		choice := strings.TrimSpace(scanner.Text())
		if choice == "2" {
			useStreaming = false
			fmt.Println(utils.Blue + "Mode: Complete response (without streaming)" + utils.Reset)
		} else {
			fmt.Println(utils.Green + "Mode: Streaming" + utils.Reset)
		}
	}
	fmt.Println(strings.Repeat("-", 50))

	for {
		fmt.Print(utils.Green + "You: " + utils.Reset)
		if !scanner.Scan() {
			break
		}

		userInput := strings.TrimSpace(scanner.Text())

		if strings.ToLower(userInput) == "quit" ||
			strings.ToLower(userInput) == "exit" {
			fmt.Println(utils.Blue + "👋 Goodbye!" + utils.Reset)
			break
		}

		if userInput == "" {
			continue
		}

		fmt.Print(utils.Blue + "Agno: " + utils.Reset)

		if useStreaming {
			// Streaming mode: real-time response
			err := api.SendToAgnoStream(userInput)
			if err != nil {
				fmt.Printf(utils.Red+"❌ Error: %v"+utils.Reset+"\n", err)
				continue
			}
		} else {
			// Complete mode: response once
			response, err := api.SendToAgno(userInput)
			if err != nil {
				fmt.Printf(utils.Red+"❌ Error: %v"+utils.Reset+"\n", err)
				continue
			}
			fmt.Println(response)
		}

		fmt.Println(strings.Repeat("-", 50))
	}
}
