package dto

import (
	"errors"
	"net/http"

	"github.com/go-chi/render"
	usecasedto "github.com/ryansakurai/harmonics-api/internal/artist/use-case/dto"
)

type ErrorResponse struct {
	HTTPStatusCode int    `json:"-"`
	Code           string `json:"code"`
	Message        string `json:"message"`
}

func (e *ErrorResponse) Render(w http.ResponseWriter, r *http.Request) error {
	render.Status(r, e.HTTPStatusCode)
	return nil
}

func ErrToRenderer(err error) render.Renderer {
	var artistNotFound *usecasedto.ArtistNotFound

	switch {
	case errors.As(err, &artistNotFound):
		return ErrArtistNotFound(err)
	default:
		return nil
	}
}

func ErrArtistNotFound(err error) render.Renderer {
	return &ErrorResponse{
		HTTPStatusCode: http.StatusNotFound,
		Code:           "ARTIST_NOT_FOUND",
		Message:        err.Error(),
	}
}
