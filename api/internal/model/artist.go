package model

type Artist struct {
	ID            string
	Name          string
	Genres        []string
	Bio           string
	QtFollowers   uint64
	AverageRating float64
	Releases      []ReleasePreview
}
