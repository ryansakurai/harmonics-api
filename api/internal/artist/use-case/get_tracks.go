package usecase

import (
	"github.com/ryansakurai/harmonics-api/internal/artist/use-case/dto"
)

func (u *ArtistUseCases) GetTracks(artistID string) (dto.Tracks, error) {
	return dto.Tracks{
		Artist: dto.Reference{
			ID:   artistID,
			Name: "The Beatles",
		},
		Items: []dto.Item{
			{
				Name: "Come Together",
				Releases: []dto.Reference{
					{
						ID:   "1",
						Name: "Abbey Road",
					},
				},
			},
			{
				Name: "Let It Be",
				Releases: []dto.Reference{
					{
						ID:   "3",
						Name: "Let It Be",
					},
				},
			},
			{
				Name: "Hey Jude",
				Releases: []dto.Reference{
					{
						ID:   "4",
						Name: "Hey Jude (Single)",
					},
				},
			},
		},
	}, nil
	// return dto.Tracks{}, &dto.ArtistNotFound{ArtistID: artistID}
}
