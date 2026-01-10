// Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

/*
agno_client.go
==============
API package for communication with the Agno server.
Contains functions for HTTP interaction with the Python FastAPI server.

MAIN FEATURES
---------------
✓ HTTP communication with the Agno server
✓ Support for streaming and complete response
✓ Server health check
✓ JSON serialization/deserialization
*/
package api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

// AgnoServerURL is the base URL of the Agno server:
const AgnoServerURL = "http://localhost:8000"

// Data models to send and receive JSON
// ChatRequest represents the request structure for the Agno server:
type ChatRequest struct {
	Message string `json:"message"`
}

// ChatResponse represents the response structure for the Agno server:
type ChatResponse struct {
	Response string `json:"response"`
}

// sendToAgno sends a message to Agno and receives a complete response (without streaming).
// Uses the /chat endpoint that returns JSON structured.
// Returns the response and error in case of failure.
func SendToAgno(message string) (string, error) {
	reqBody := ChatRequest{Message: message}
	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return "", err
	}

	resp, err := http.Post(
		AgnoServerURL+"/chat",
		"application/json",
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	// Deserialize JSON response using ChatResponse:
	var chatResp ChatResponse
	err = json.NewDecoder(resp.Body).Decode(&chatResp)
	if err != nil {
		return "", err
	}

	return chatResp.Response, nil
}

// sendToAgnoStream sends a message to Agno and receives a streaming response.
// Uses the /chat/stream endpoint that returns text in real time.
// Returns error in case of failure.
func SendToAgnoStream(message string) error {
	reqBody := ChatRequest{Message: message}
	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return err
	}

	resp, err := http.Post(
		AgnoServerURL+"/chat/stream",
		"application/json",
		bytes.NewBuffer(jsonData), // create a "stream" of bytes for the request body
	)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Read and print chunk by chunk:
	buf := make([]byte, 1024)
	for {
		n, err := resp.Body.Read(buf) // Read up to 1024 bytes
		if n > 0 {
			fmt.Print(string(buf[:n]))
		}
		if err == io.EOF {
			break
		}
		if err != nil {
			return err
		}
	}
	fmt.Println()
	return nil
}

// CheckServerHealth checks if the Agno server is running
// Returns true if the server is accessible, false otherwise
func CheckServerHealth() bool {
	resp, err := http.Get(AgnoServerURL + "/health")
	if err != nil {
		return false
	}
	defer resp.Body.Close()
	return resp.StatusCode == 200
}
