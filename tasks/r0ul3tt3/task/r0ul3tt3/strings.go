package main

import (
	"net"
	"time"
)

var CHEER = "Place the bets!\n"

var BANNER = "Welcome to the greatest casino!\n" +
	"Roulette is spinning, your bet is winning!\n" +
	"Type 'help' if you don't know the rules\n\n" +
	"Your initial capital is 100$\n"

var HELP = "Rules are simple:\n" +
	"- type 'red' to place on red sector\n" +
	"- type 'black' to place on black sector\n" +
	"- type number from 0 to 36 to place on it\n" +
	"- type 'status' to show your current capital\n" +
	"- type 'exit' quit this game\n\n" +
	"Getting 1000000$ makes you a winner.\n"

var GOODBYE = "See ya!\n"

var NONSENSE = "Sorry, can't really get you.\nType 'help' to get reference.\n"

var DEFEAT = "Game over!\n"

var VICTORY = "My congratulations!\nHere is your flag:!\n"

var REDBET = "You bet on red!\nHow much you wanna place?\n"

var BLACKBET = "You bet on black!\nHow much you wanna place?\n"

func printSpinMessage(conn net.Conn) {
	_, _ = conn.Write([]byte("The bet has been accepted.\n"))
	time.Sleep(DELAY * 2)
	_, _ = conn.Write([]byte("Spinning the roulette...\n"))
	time.Sleep(DELAY)
	_, _ = conn.Write([]byte(".\n"))
	time.Sleep(DELAY)
	_, _ = conn.Write([]byte("..\n"))
	time.Sleep(DELAY)
	_, _ = conn.Write([]byte("...\n"))
}
