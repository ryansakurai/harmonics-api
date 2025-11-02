package dto

import (
	"net/http"

	"github.com/go-chi/render"
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

func ErrArtistNotFound(err error) render.Renderer {
	return &ErrorResponse{
		HTTPStatusCode: http.StatusNotFound,
		Code:           "ARTIST_NOT_FOUND",
		Message:        err.Error(),
	}
}
