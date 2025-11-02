package handler

import (
	"errors"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/render"
	"github.com/ryansakurai/harmonics-api/internal/artist/handler/dto"
	usecasedto "github.com/ryansakurai/harmonics-api/internal/artist/use-case/dto"
)

func (h *ArtistHandler) ServeGetArtist(w http.ResponseWriter, r *http.Request) {
	artistID := chi.URLParam(r, "artistID")

	artist, err := h.useCase.GetArtist(artistID)
	if err != nil {
		render.Render(w, r, errToRenderer(err))
		return
	}

	render.Render(w, r, toPayload(artist))
}

func errToRenderer(err error) render.Renderer {
	var artistNotFound *usecasedto.ArtistNotFound

	switch {
	case errors.As(err, &artistNotFound):
		return dto.ErrArtistNotFound(err)
	default:
		return nil
	}
}

func toPayload(artist usecasedto.Artist) dto.GetArtistPayload {
	releases := make([]dto.ReleasePreview, len(artist.Releases))
	for i, release := range artist.Releases {
		releases[i] = dto.ReleasePreview{
			ID:          release.ID,
			Name:        release.Name,
			ReleaseYear: release.ReleaseYear,
		}
	}

	return dto.GetArtistPayload{
		ID:            artist.ID,
		Name:          artist.Name,
		Genres:        artist.Genres,
		Bio:           artist.Bio,
		QtFollowers:   artist.QtFollowers,
		AverageRating: artist.AverageRating,
		Releases:      releases,
	}
}
