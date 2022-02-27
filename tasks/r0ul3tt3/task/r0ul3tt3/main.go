package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"math/rand"
	"net"
	"os"
	"strconv"
	"strings"
	"time"
)

var DELAY = 700 * time.Millisecond
var FLAG = os.Getenv("FLAG")

var RED = []string{"1", "3", "5", "7", "9", "12", "14", "16", "18", "19", "21", "23", "25", "27", "30", "32", "34", "36"}
var BLACK = []string{"2", "4", "6", "8", "10", "11", "13", "15", "17", "20", "22", "24", "26", "28", "29", "31", "33", "35"}

var NUMBERS = append(append(RED, BLACK...), "0")

func doBet(conn net.Conn, scanner *bufio.Scanner, money *int, pull []string) error {
	scanner.Scan()
	data := scanner.Text()

	amount, err := strconv.Atoi(data)
	if err != nil {
		return errors.New("Is your number valid integer?..")
	}

	if amount > *money {
		return errors.New("You don't have enough money!")
	}

	*money -= amount
	printSpinMessage(conn)

	r := rand.Intn(37)
	res := strconv.Itoa(r)
	_, _ = conn.Write([]byte("It's " + res + "!\n"))

	if stringInSlice(res, pull) {
		prize := amount
		if len(pull) == 1 {
			prize *= 10
		} else {
			prize *= 2
		}
		*money += prize
		_, _ = conn.Write([]byte("You won " + strconv.Itoa(prize) + "$!\n"))
	} else {
		_, _ = conn.Write([]byte("You lost this bet.\n"))
	}

	return nil
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	money := 100
	_, _ = conn.Write([]byte(BANNER + "\n"))
	_, _ = conn.Write([]byte(CHEER + "\n"))

	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		message := scanner.Text()
		message = strings.TrimSpace(message)
		message = strings.Trim(message, "\n")

		if message == "help" {
			_, _ = conn.Write([]byte(HELP + "\n"))
		} else if message == "quit" {
			_, _ = conn.Write([]byte(GOODBYE + "\n"))
			return
		} else if message == "status" {
			_, _ = conn.Write([]byte(strconv.Itoa(money) + "$ on your account\n"))
		} else if message == "black" {
			_, _ = conn.Write([]byte(BLACKBET))
			err := doBet(conn, scanner, &money, BLACK)
			if err != nil {
				_, _ = conn.Write([]byte(err.Error() + "\n"))
			}
		} else if message == "red" {
			_, _ = conn.Write([]byte(REDBET))
			err := doBet(conn, scanner, &money, RED)
			if err != nil {
				_, _ = conn.Write([]byte(err.Error() + "\n"))
			}
		} else if stringInSlice(message, NUMBERS) {
			_, _ = conn.Write([]byte("You bet on " + message + "!\nHow much you wanna place?\n"))
			err := doBet(conn, scanner, &money, []string{message})
			if err != nil {
				_, _ = conn.Write([]byte(err.Error() + "\n"))
			}
		} else {
			_, _ = conn.Write([]byte(NONSENSE + "\n"))
		}

		if money <= 0 {
			_, _ = conn.Write([]byte(DEFEAT + "\n"))
			return
		}

		if money >= 10000000 {
			_, _ = conn.Write([]byte(VICTORY + "\n"))
			_, _ = conn.Write([]byte(FLAG + "\n"))
			return
		}

		_, _ = conn.Write([]byte(CHEER + "\n"))
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("error:", err)
	}
}

func main() {
	ln, err := net.Listen("tcp", "0.0.0.0:8080")
	if err != nil {
		panic(err)
	}

	fmt.Println("Accept connections on port 8080")
	for {
		conn, err := ln.Accept()
		if err != nil {
			panic(err)
		}
		_ = conn.SetDeadline(time.Time{})

		log.Println(conn.RemoteAddr())
		go handleConnection(conn)
	}
}
