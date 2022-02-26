package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/go-redis/redis/v8"
	"github.com/google/uuid"
	"github.com/gorilla/mux"
	log "github.com/sirupsen/logrus"
	"html/template"
	"net/http"
	"os"
	"strconv"
	"strings"
)

/* MODELS */

type Lookup struct {
	IP          string `json:"ip"`
	CountryCode string `json:"country_code"`
	CountryName string `json:"country_name"`
}

type UserTemplate struct {
	UserID     string
	Countries  []string
	Flag1      string
	Flag2      string
	Flag3      string
	Error      string
}

/* LOOKUP */

var GEOAPI = "https://freegeoip.app/json/"

func getLookupByIP(ip string) (*Lookup, error) {
	log.Debug("Looking for " + ip)

	res, err := http.Get(GEOAPI + ip)
	if err != nil {
		return nil, err
	}

	defer res.Body.Close()

	var lookup Lookup
	err = json.NewDecoder(res.Body).Decode(&lookup)

	log.Info(lookup)
	return &lookup, err
}

/* DB */

var rdb = redis.NewClient(&redis.Options{
	Addr:     os.Getenv("REDIS_ADDRESS"),
	Password: "", // no password set
	DB:       0,  // use default DB
})

func getUserID(username string, password string) (userID string, err error) {
	var ctx = context.Background()

	res := rdb.Get(ctx, "user:" + username + ":" + password)
	return res.Result()
}

func createUser(username string, password string) (userID string, err error) {
	var ctx = context.Background()

	existingUser, err := getUserID(username, password)
	if err != redis.Nil {
		return "", err
	}
	if existingUser != "" {
		log.Warn(existingUser)
		return "", errors.New("пользователь существует")
	}

	id := uuid.New()
	rdb.Set(ctx, "user:" + username + ":" + password, id.String(), 0)

	return id.String(), nil
}

func getTemplateDataByCookie(cookie *http.Cookie) UserTemplate {
	var ctx = context.Background()

	userID, err := rdb.Get(ctx, "user:" + cookie.Value).Result()
	if err == redis.Nil {
		return UserTemplate{Error: "пользователя не существует"}
	}

	countries, err := rdb.SMembers(ctx, "id:" + userID).Result()
	if err != redis.Nil && err != nil{
		return UserTemplate{Error: err.Error()}
	}

	user := UserTemplate{
		UserID: userID,
		Countries: countries,
	}

	if len(countries) >= 3 {
		user.Flag1 = "HITS{n0w_y0u_kn0w_th3_r00l5}"
	}
	if len(countries) >= 9 {
		user.Flag2 = "HITS{4dv3ntur3_15_ju57_b3gun}"
	}
	if len(countries) >= 18 {
		user.Flag3 = "HITS{y0u_c4n_h4v3_y0ur_c0r0n4_n0w}"
	}

	return user
}

func addCountryByUserID(country string, userID string) {
	var ctx = context.Background()

	res := rdb.SAdd(ctx, "id:" + userID, country)
	code, err := res.Result()
	if err != nil {
		log.Error("Add country " + country + " for user " + userID + ", error: " + err.Error())
	} else {
		log.Info("Add country " + country + " for user " + userID + ", result: " + strconv.Itoa(int(code)))
	}
}

/* PAGES */

func indexPageHandler(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("templates/index.html"))

	cookie, err := r.Cookie("user")
	if err != nil {
		_ = tmpl.Execute(w, UserTemplate{Error: err.Error()})
		return
	}

	_ = tmpl.Execute(w, getTemplateDataByCookie(cookie))
}

func travelPageHandler(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("templates/travel.html"))

	params := mux.Vars(r)
	userID := params["id"]
	ip := strings.Split(r.RemoteAddr, ":")[0]

	lookup, err := getLookupByIP(ip)
	if err != nil {
		log.Error(err)
		_ = tmpl.Execute(w, lookup)
		return
	}

	if lookup.CountryCode != "" {
		addCountryByUserID(lookup.CountryCode, userID)
	}

	_ = tmpl.Execute(w, lookup)
}

func adminPageHandler(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("templates/admin.html"))

	cookie, err := r.Cookie("user")
	if err != nil {
		log.Error(err)
		http.Redirect(w, r, "/", http.StatusSeeOther)
		return
	}

	_ = tmpl.Execute(w, getTemplateDataByCookie(cookie))
}

func loginPageHandler(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("templates/login.html"))

	if r.Method == http.MethodGet {
		_ = tmpl.Execute(w, UserTemplate{})
	} else {
		err := r.ParseForm()
		if err != nil {
			log.Error(err)
			_ = tmpl.Execute(w, UserTemplate{Error: err.Error()})
			return
		}

		username := r.FormValue("username")
		password := r.FormValue("password")

		userID, err := getUserID(username, password)
		if userID == "" {
			_ = tmpl.Execute(w, UserTemplate{Error: "пользователь не найден"})
			return
		}

		cookie := &http.Cookie{
			Name:   "user",
			Value:  username + ":" + password,
			MaxAge: 60 * 60 * 3,
		}

		http.SetCookie(w, cookie)
		http.Redirect(w, r, "/admin", http.StatusSeeOther)
	}
}

func registerPageHandler(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("templates/register.html"))

	if r.Method == http.MethodGet {
		_ = tmpl.Execute(w, UserTemplate{})
	} else {
		err := r.ParseForm()
		if err != nil {
			_ = tmpl.Execute(w, UserTemplate{Error: err.Error()})
			log.Error(err)
			return
		}

		username := r.FormValue("username")
		password := r.FormValue("password")

		_, err = createUser(username, password)
		if err != nil {
			log.Error(err)
			_ = tmpl.Execute(w, UserTemplate{Error: err.Error()})
			return
		}

		http.Redirect(w, r, "/login", http.StatusSeeOther)
	}
}

/* MAIN */

func init() {
	log.SetOutput(os.Stdout)
	log.SetLevel(log.DebugLevel)
	log.SetReportCaller(true)
}

var logPath = func(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/ping" {
			log.Info(fmt.Sprintf("%s: %s %s (%s)", r.RemoteAddr, r.Method, r.RequestURI, r.UserAgent()))
		}
		next.ServeHTTP(w, r)
	})
}

func main() {
	r := mux.NewRouter()

	r.HandleFunc("/", indexPageHandler).Methods(http.MethodGet)
	r.HandleFunc("/register", registerPageHandler).Methods(http.MethodGet, http.MethodPost)
	r.HandleFunc("/login", loginPageHandler).Methods(http.MethodGet, http.MethodPost)
	r.HandleFunc("/admin", adminPageHandler).Methods(http.MethodGet)
	r.HandleFunc("/travel/{id}", travelPageHandler).Methods(http.MethodGet)

	r.Use(logPath) // middleware

	port := os.Getenv("PORT")
	if port == "" {
		port = "8090" // localhost
	}

	log.Info("Listening on: ", port)

	err := http.ListenAndServe(":"+port, r)
	if err != nil {
		log.Panic(err)
	}
}
