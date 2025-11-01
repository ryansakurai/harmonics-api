package artist

import (
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/render"

	"github.com/ryansakurai/harmonics-api/internal/dto/response"
	"github.com/ryansakurai/harmonics-api/internal/library"
	"github.com/ryansakurai/harmonics-api/internal/model"
)

func (h *ArtistHandler) ServeGetArtist(w http.ResponseWriter, r *http.Request) {
	artistID := chi.URLParam(r, "artistID")

	artist, err := h.useCase.GetArtist(artistID)
	if err != nil {
		render.Render(w, r, library.ErrorToRenderer(err))
		return
	}

	render.Render(w, r, modelToResponse(artist))
}

func modelToResponse(model model.Artist) response.GetArtistResponse {
	releases := make([]response.ReleasePreview, len(model.Releases))
	for i, release := range model.Releases {
		releases[i] = response.ReleasePreview{
			ID:          release.ID,
			Name:        release.Name,
			ReleaseYear: release.ReleaseYear,
		}
	}

	return response.GetArtistResponse{
		ID:            model.ID,
		Name:          model.Name,
		Genres:        model.Genres,
		Bio:           model.Bio,
		QtFollowers:   model.QtFollowers,
		AverageRating: model.AverageRating,
		Releases:      releases,
	}
}
