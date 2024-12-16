package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

var clients []net.Conn

func broadcastMessage(message string, sender net.Conn) {
	for _, client := range clients {
		if client != sender {
			client.Write([]byte(message))
		}
	}
}

func handleClient(conn net.Conn) {
	defer conn.Close()
	// add client to list
	clients = append(clients, conn)
	fmt.Println("New Client connected: ", conn.RemoteAddr())

	for {
		message, err := bufio.NewReader(conn).ReadString('\n')
		if err != nil {
			fmt.Println("Client disconnected :", conn.RemoteAddr())
			//remove client address
			for i, client := range clients {
				if client == conn {
					clients = append(clients[:i], clients[:i+1]...)
					break
				}
			}
			return
		}
		// broad cast message to other clients
		message = strings.TrimSpace(message)
		fmt.Println("Message recieved :", message)
		broadcastMessage(message+"\n", conn)

	}

}
func main() {
	listener, err := net.Listen("tcp", "0.0.0.0:12345")
	if err != nil {
		fmt.Println("Error starting server.", err)
		os.Exit(1)
	}
	defer listener.Close()

	fmt.Println("Server is listening on 0.0.0.0:12345")
	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error Accepting connection: ", err)
			continue
		}
		go handleClient(conn)
	}
}
