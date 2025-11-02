package dto

import "net/http"

type GetTracksPayload struct {
	Artist Reference `json:"artist"`
	Items  []Item    `json:"items"`
}

type Reference struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type Item struct {
	Name     string      `json:"name"`
	Releases []Reference `json:"releases"`
}

func (g GetTracksPayload) Render(w http.ResponseWriter, r *http.Request) error {
	return nil
}
