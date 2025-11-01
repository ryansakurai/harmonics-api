package response

import "net/http"

type GetArtistResponse struct {
	ID            string           `json:"id"`
	Name          string           `json:"name"`
	Genres        []string         `json:"genres"`
	Bio           string           `json:"bio"`
	QtFollowers   uint64           `json:"qtFollowers"`
	AverageRating float64          `json:"averageRating"`
	Releases      []ReleasePreview `json:"releases"`
}

type ReleasePreview struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	ReleaseYear string `json:"releaseYear"`
}

func (g GetArtistResponse) Render(w http.ResponseWriter, r *http.Request) error {
	return nil
}
