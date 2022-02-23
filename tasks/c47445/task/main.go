package main

import (
	"encoding/json"
	"fmt"
	"github.com/google/uuid"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

var API = "https://cataas.com"

var PORT = os.Getenv("PORT")

var FLAG1 = os.Getenv("FLAG1")
var FLAG2 = os.Getenv("FLAG2")

var DIR = "/tmp"

type SecretBody struct {
	UserUUID     string
	ServerSecret string
}

func GetCat(w http.ResponseWriter, req *http.Request) {
	id := uuid.New().String()
	go sendRequest(id)

	message := "Your cat is waiting for you at /cats?id=" + id
	_, _ = fmt.Fprint(w, message)
}

func sendRequest(id string) {
	filename := DIR + "/" + id

	sb := SecretBody{ServerSecret: FLAG2, UserUUID: id}
	b, _ := json.Marshal(sb)

	// let's store it locally first
	// might be useful for debug purpose
	// it will be overwritten by image anyway
	err := ioutil.WriteFile(filename, b, 0644)
	if err != nil {
		log.Println(err)
		return
	}

	res, err := http.Get(API + "/cat" + "?user_id=" + sb.UserUUID + "&app_secret=" + sb.ServerSecret)
	if err != nil {
		log.Println(err)
		return
	}

	responseData, err := ioutil.ReadAll(res.Body)
	if err != nil {
		log.Println(err)
		return
	}

	err = ioutil.WriteFile(filename, responseData, 0644)
	if err != nil {
		log.Println(err)
		return
	}
}

func ShowCat(w http.ResponseWriter, req *http.Request) {
	id := req.URL.Query().Get("id")
	filename := DIR + "/" + id

	data, err := ioutil.ReadFile(filename)
	if err != nil {
		handleError(w, err)
		return
	}

	_, _ = fmt.Fprint(w, string(data))
}

func handleError(w http.ResponseWriter, err error) {
	log.Println(err)
	http.Error(w, err.Error(), http.StatusInternalServerError)
}

func init() {
	err := ioutil.WriteFile("/secret/flag.txt", []byte(FLAG1), 0644)
	if err != nil {
		panic(err)
	}
}

func main() {
	http.HandleFunc("/", GetCat)
	http.HandleFunc("/cats", ShowCat)

	if PORT == "" {
		PORT = "8080"
	}

	log.Println("Listening on: " + PORT)
	err := http.ListenAndServe(":"+PORT, nil)
	if err != nil {
		panic(err)
	}
}
