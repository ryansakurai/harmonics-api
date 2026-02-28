package main

import (
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/render"

	artisthandler "github.com/sakuraven/harmonics-api/internal/artist/handler"
	artistusecase "github.com/sakuraven/harmonics-api/internal/artist/use-case"
	followhandler "github.com/sakuraven/harmonics-api/internal/follow/handler"
	friendhandler "github.com/sakuraven/harmonics-api/internal/friend/handler"
	ratinghandler "github.com/sakuraven/harmonics-api/internal/rating/handler"
	recommendationhandler "github.com/sakuraven/harmonics-api/internal/recommendation/handler"
	releasehandler "github.com/sakuraven/harmonics-api/internal/release/handler"
	userhandler "github.com/sakuraven/harmonics-api/internal/user/handler"
)

func main() {
	artistUseCase := artistusecase.New()

	artistHandler := artisthandler.New(artistUseCase)
	releaseHandler := releasehandler.New()
	userHandler := userhandler.New()
	friendHandler := friendhandler.New()
	ratingHandler := ratinghandler.New()
	followHandler := followhandler.New()
	recommendationHandler := recommendationhandler.New()

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
			r.Get("/", artistHandler.ServeGetArtist)
			r.Get("/tracks", artistHandler.ServeGetTracks)
		})

		r.Route("/releases/{releaseID}", func(r chi.Router) {
			r.Get("/", releaseHandler.ServeGetRelease)
			r.Get("/ratings", releaseHandler.ServeGetRatings)
		})

		r.Route("/users", func(r chi.Router) {
			r.Post("/", userHandler.ServePostUser)

			r.Route("/{username}", func(r chi.Router) {
				r.Get("/", userHandler.ServeGetUser)
				r.Delete("/", userHandler.ServeDeleteUser)
				r.Patch("/", userHandler.ServePatchUser)

				r.Route("/friends", func(r chi.Router) {
					r.Get("/", friendHandler.ServeGetFriends)
					r.Post("/", friendHandler.ServePostFriend)
					r.Delete("/{friendUsername}", friendHandler.ServeDeleteFriend)
				})

				r.Route("/ratings", func(r chi.Router) {
					r.Get("/", ratingHandler.ServeGetRatings)
					r.Post("/", ratingHandler.ServePostRating)
					r.Delete("/{releaseID}", ratingHandler.ServeDeleteRating)
				})

				r.Route("/follows", func(r chi.Router) {
					r.Get("/", followHandler.ServeGetFollows)
					r.Post("/", followHandler.ServePostFollow)
					r.Delete("/{artistID}", followHandler.ServeDeleteFollow)
				})

				r.Route("/recommendations", func(r chi.Router) {
					r.Get("/artists", recommendationHandler.ServeGetArtists)
					r.Get("/releases", recommendationHandler.ServeGetReleases)
					r.Get("/friends", recommendationHandler.ServeGetFriends)
				})
			})
		})
	})

	http.ListenAndServe(":3333", r)
}
