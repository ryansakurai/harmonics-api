package user

import (
	"github.com/ryansakurai/harmonics-api/internal/handler/user/follow"
	"github.com/ryansakurai/harmonics-api/internal/handler/user/friend"
	"github.com/ryansakurai/harmonics-api/internal/handler/user/rating"
	"github.com/ryansakurai/harmonics-api/internal/handler/user/recommendation"
)

type UserHandler struct {
	FriendHandler         *friend.FriendHandler
	RatingHandler         *rating.RatingHandler
	FollowHandler         *follow.FollowHandler
	RecommendationHandler *recommendation.RecommendationHandler
}

func New() *UserHandler {
	return &UserHandler{
		FriendHandler:         friend.New(),
		RatingHandler:         rating.New(),
		FollowHandler:         follow.New(),
		RecommendationHandler: recommendation.New(),
	}
}
