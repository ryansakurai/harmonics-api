package handler

import (
	usecasedto "github.com/ryansakurai/harmonics-api/internal/artist/use-case/dto"
)

type ArtistHandler struct {
	useCase ArtistUseCases
}

type ArtistUseCases interface {
	GetArtist(artistID string) (usecasedto.Artist, error)
}

func New(useCase ArtistUseCases) *ArtistHandler {
	return &ArtistHandler{
		useCase: useCase,
	}
}
