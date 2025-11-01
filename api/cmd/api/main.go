package main

import (
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/render"
)

func main() {
	r := chi.NewRouter()

	r.Use(middleware.RequestID)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Timeout(60 * time.Second))

	r.Route("/api/v2", func(r chi.Router) {
		r.Get("/", func(w http.ResponseWriter, r *http.Request) {
			render.Status(r, http.StatusOK)
		})

		r.Route("/artists/{artistID}", func(r chi.Router) {
			r.Get("/", func(w http.ResponseWriter, r *http.Request) {})
			r.Get("/tracks", func(w http.ResponseWriter, r *http.Request) {})
		})

		r.Route("/releases/{releaseID}", func(r chi.Router) {
			r.Get("/", func(w http.ResponseWriter, r *http.Request) {})
			r.Get("/ratings", func(w http.ResponseWriter, r *http.Request) {})
		})

		r.Route("/users", func(r chi.Router) {
			r.Post("/", func(w http.ResponseWriter, r *http.Request) {})

			r.Route("/{username}", func(r chi.Router) {
				r.Get("/", func(w http.ResponseWriter, r *http.Request) {})
				r.Delete("/", func(w http.ResponseWriter, r *http.Request) {})
				r.Patch("/", func(w http.ResponseWriter, r *http.Request) {})

				r.Route("/friends", func(r chi.Router) {
					r.Get("/", func(w http.ResponseWriter, r *http.Request) {})
					r.Post("/", func(w http.ResponseWriter, r *http.Request) {})
					r.Delete("/{friendUsername}", func(w http.ResponseWriter, r *http.Request) {})
				})

				r.Route("/ratings", func(r chi.Router) {
					r.Get("/", func(w http.ResponseWriter, r *http.Request) {})
					r.Post("/", func(w http.ResponseWriter, r *http.Request) {})
					r.Delete("/{releaseID}", func(w http.ResponseWriter, r *http.Request) {})
				})

				r.Route("/follows", func(r chi.Router) {
					r.Get("/", func(w http.ResponseWriter, r *http.Request) {})
					r.Post("/", func(w http.ResponseWriter, r *http.Request) {})
					r.Delete("/{artistID}", func(w http.ResponseWriter, r *http.Request) {})
				})

				r.Route("/recommendations", func(r chi.Router) {
					r.Get("/artists", func(w http.ResponseWriter, r *http.Request) {})
					r.Get("/releases", func(w http.ResponseWriter, r *http.Request) {})
					r.Get("/friends", func(w http.ResponseWriter, r *http.Request) {})
				})
			})
		})
	})

	http.ListenAndServe(":3333", r)
}
