from django.urls import path
from . import views
urlpatterns = [
    path('',views.ApiOverview,name="apioverview"),
    path('Posts/',views.Posts,name="posts"),
    path('Get_By_Id/<str:pk>/',views.Get_Posts_By_id,name="get_by_id"),
    path('Create_Post/',views.Create_Post,name="Create_Post"),
    path('Delete_Post/<str:pk>/',views.Delete_Post,name="Delete_Post"),
    path('Update_Post/<str:pk>/',views.Update_Post,name="Update_Post"),
    path('Like_Post/<str:pk>/',views.like_post,name="Like_Post"),
    path('dislike_Post/<str:pk>/',views.dislike_post,name="dislike_Post"),
    path('comment/<str:pk>/',views.comment,name="comment_Post"),
    path('comments/',views.showallcomment,name="showallcomment"),
    path('like_comment/<str:pk>/',views.like_comment,name="like_comment"),
    path('dislike_comment/<str:pk>/',views.dislike_comment,name="dislike_comment"),
]
