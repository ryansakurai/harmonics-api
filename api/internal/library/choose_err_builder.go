package library

import (
	"errors"

	"github.com/go-chi/render"

	"github.com/ryansakurai/harmonics-api/internal/dto/erring"
	"github.com/ryansakurai/harmonics-api/internal/dto/response"
)

func ErrorToRenderer(err error) render.Renderer {
	var artistNotFound *erring.ArtistNotFound

	switch {
	case errors.As(err, &artistNotFound):
		return response.ErrArtistNotFound(err)
	default:
		return response.ErrInternalServer()
	}
}
