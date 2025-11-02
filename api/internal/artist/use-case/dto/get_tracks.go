package dto

type Tracks struct {
	Artist Reference
	Items  []Item
}

type Reference struct {
	ID   string
	Name string
}

type Item struct {
	Name     string
	Releases []Reference
}
