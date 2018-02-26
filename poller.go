package main

import (
"os"
"fmt"
"bufio"
"time"
"net/http"
//"encoding/json"
)

const (
	NEWS_API_HEADLINES = "https://newsapi.org/v2/top-headlines?q="
	NEWS_API_KEY_QUERY = "&apiKey="
	BAD_REQUEST_CODE = 10
	//NEWS_API_EVERTHING = "https://newsapi.org/v2/everything?q="
	//NEWS_API_DATE_FORMAT = "&from="
	//NEWS_API_MISC= "&sortBy=popularity&apiKey="
	//BAD_JSON_UNMARSHAL = 9
)

type ArticleSearch struct {
	errcode int
	timestamp string
	articles []byte
	//articles map[string]interface{}
}

type RoutineResult struct {
	errcode int
	keyword string 
	articles []byte
	//articles map[string]interface{}
}

func main() {
	//parse keywords from config.txt, populate keywords, apikey variables
	reader := bufio.NewReader(os.Stdin)
	config, _ := reader.ReadString('\n')
	keywords = make([]string, 0)
	var apikey string

	for i := 0; i < len(config); i++ {
		if config[i] == "apikey:" {
			apikey = config[i+1]
			break
		}
		if config[i] != "keywords:"{
			keywords = append(&keywords, config[i])
		}
	}

	//populate allSearches map with keyword:ArticleSearch skeletons 
	currentTime := time.Now().Local()
	allSearches := make(map[string]ArticleSearch, 0)
	for i := 0; i < len(keywords); i++ {
		//articlesMap = make(map[string]interface{})
		//a := ArticleSearch{errcode: 0, timestamp: currentTime, articles: articlesMap}
		a := ArticleSearch{errcode: 0, timestamp: currentTime, articles: nil}
		allSearches[keywords[i].(string)] = a
	}

	//make channel, call getArticles func on all keywords && store results from channel
	allSearchesLen := len(allSearches)
	articlesChan := make(chan RoutineResult, allSearchesLen) 
	for i := 0; i < allSearchesLen; i++ {
		go allSearches[keywords[i].(string)].getArticles(articlesChan, apikey)
	}

	for i := 0; i < allSearchesLen; i++ {
		keyword, articles := <-articlesChan
		allSearches[keyword].articles = articles
	}
	close(articlesChan)

	//to STDOUT: separate for purpose of removing additional overhead of printing 
	fmt.Println("OUT_START")
	for i := 0; i < allSearchesLen; i++ {
		kwd := keywords[i]
		asObj := allSearches[kwd.(string)]
		if asObj.errcode != 0 {
			fmt.Println(kwd)
			asObj.toSTDOUT() 
		}
	}
	fmt.Println("OUT_END")
}

func (ArticleSearch) getArticles(ch chan<- RoutineResult, apikey string) {
	
	//compose request URL, make get request for articles 
	url := NEWS_API_HEADLINES + a.keyword + NEWS_API_KEY_QUERY + apikey 
	var result RoutineResult
	result.keyword = a.keyword

	//make get request for articles, parse json if no error code 
	resp, err := http.Get(url)
	if err != nil {
		a.errcode = BAD_REQUEST_CODE
	} else {
		a.articles = resp
		/*
		var out map[string]interface{}
		parseErr := json.Unmarshal(resp, &out)
		if parseErr != nil {
			a.errcode = BAD_JSON_UNMARSHAL
		} else {
			result.articles = out
		}
		*/
	}

	ch <- result
}

func (ArticleSearch) toSTDOUT(){
	fmt.Println("@S@")
	fmt.Println(a.timestamp)
	fmt.Println(a.articles)
	fmt.Println("@E@")
}