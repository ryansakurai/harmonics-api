package erring

import "fmt"

type ArtistNotFound struct {
	ArtistID string
}

func (a *ArtistNotFound) Error() string {
	return fmt.Sprintf("artist with ID %s not found", a.ArtistID)
}
