package usecase

import (
	"github.com/ryansakurai/harmonics-api/internal/artist/use-case/dto"
)

func (u *ArtistUseCases) GetArtist(artistID string) (dto.Artist, error) {
	return dto.Artist{
		ID:            artistID,
		Name:          "The Beatles",
		Genres:        []string{"Rock", "Pop", "Psychedelic Rock"},
		Bio:           "The Beatles were an English rock band formed in Liverpool in 1960.",
		QtFollowers:   1000000,
		AverageRating: 4.8,
		Releases: []dto.ReleasePreview{
			{
				ID:          "1",
				Name:        "Abbey Road",
				ReleaseYear: "1969",
			},
			{
				ID:          "2",
				Name:        "Sgt. Pepper's Lonely Hearts Club Band",
				ReleaseYear: "1967",
			},
		},
	}, nil
	// return dto.Artist{}, &dto.ArtistNotFound{ArtistID: artistID}
}
