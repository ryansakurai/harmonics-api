package handler

import (
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/render"
	"github.com/ryansakurai/harmonics-api/internal/artist/handler/dto"
	usecasedto "github.com/ryansakurai/harmonics-api/internal/artist/use-case/dto"
)

func (h *ArtistHandler) ServeGetTracks(w http.ResponseWriter, r *http.Request) {
	artistID := chi.URLParam(r, "artistID")

	tracks, err := h.useCase.GetTracks(artistID)
	if err != nil {
		render.Render(w, r, dto.ErrToRenderer(err))
		return
	}

	render.Render(w, r, toTracksPayload(tracks))
}

func toTracksPayload(tracks usecasedto.Tracks) dto.GetTracksPayload {
	items := make([]dto.Item, len(tracks.Items))
	for i, item := range tracks.Items {
		releases := make([]dto.Reference, len(item.Releases))
		for j, release := range item.Releases {
			releases[j] = dto.Reference{
				ID:   release.ID,
				Name: release.Name,
			}
		}
		items[i] = dto.Item{
			Name:     item.Name,
			Releases: releases,
		}
	}

	return dto.GetTracksPayload{
		Artist: dto.Reference{
			ID:   tracks.Artist.ID,
			Name: tracks.Artist.Name,
		},
		Items: items,
	}
}
