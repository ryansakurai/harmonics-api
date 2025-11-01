package artist

import "github.com/ryansakurai/harmonics-api/internal/model"

type ArtistHandler struct {
	useCase ArtistUseCases
}

type ArtistUseCases interface {
	GetArtist(artistID string) (model.Artist, error)
}

func New(useCase ArtistUseCases) *ArtistHandler {
	return &ArtistHandler{
		useCase: useCase,
	}
}
