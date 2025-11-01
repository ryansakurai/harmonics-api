package main

import (
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/render"

	artistusecase "github.com/ryansakurai/harmonics-api/internal/use-case/artist"
	artisthandler "github.com/ryansakurai/harmonics-api/internal/handler/artist"
	releasehandler "github.com/ryansakurai/harmonics-api/internal/handler/release"
	userhandler "github.com/ryansakurai/harmonics-api/internal/handler/user"
)

func main() {
	artist_use_case := artistusecase.New()

	artist_handler := artisthandler.New(artist_use_case)
	release_handler := releasehandler.New()
	userhandler := userhandler.New()

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
			r.Get("/", artist_handler.ServeGetArtist)
			r.Get("/tracks", artist_handler.ServeGetTracks)
		})

		r.Route("/releases/{releaseID}", func(r chi.Router) {
			r.Get("/", release_handler.ServeGetRelease)
			r.Get("/ratings", release_handler.ServeGetRatings)
		})

		r.Route("/users", func(r chi.Router) {
			r.Post("/", userhandler.ServePostUser)

			r.Route("/{username}", func(r chi.Router) {
				r.Get("/", userhandler.ServeGetUser)
				r.Delete("/", userhandler.ServeDeleteUser)
				r.Patch("/", userhandler.ServePatchUser)

				r.Route("/friends", func(r chi.Router) {
					r.Get("/", userhandler.FriendHandler.ServeGetFriends)
					r.Post("/", userhandler.FriendHandler.ServePostFriend)
					r.Delete("/{friendUsername}", userhandler.FriendHandler.ServeDeleteFriend)
				})

				r.Route("/ratings", func(r chi.Router) {
					r.Get("/", userhandler.RatingHandler.ServeGetRatings)
					r.Post("/", userhandler.RatingHandler.ServePostRating)
					r.Delete("/{releaseID}", userhandler.RatingHandler.ServeDeleteRating)
				})

				r.Route("/follows", func(r chi.Router) {
					r.Get("/", userhandler.FollowHandler.ServeGetFollows)
					r.Post("/", userhandler.FollowHandler.ServePostFollow)
					r.Delete("/{artistID}", userhandler.FollowHandler.ServeDeleteFollow)
				})

				r.Route("/recommendations", func(r chi.Router) {
					r.Get("/artists", userhandler.RecommendationHandler.ServeGetArtists)
					r.Get("/releases", userhandler.RecommendationHandler.ServeGetReleases)
					r.Get("/friends", userhandler.RecommendationHandler.ServeGetFriends)
				})
			})
		})
	})

	http.ListenAndServe(":3333", r)
}
