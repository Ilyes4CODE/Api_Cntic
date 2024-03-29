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
    #added 
    path('Update_Profile/',views.update_profile,name="update_profile"),
    path('Create_Event/',views.create_event,name="create_event"),
    path('Update_Event/<str:pk>/',views.update_event,name="update_event"),
    path('Delete_event/<str:pk>/',views.delete_event,name="delete_event"),
    path('Show_event/',views.Show_Event,name="Show_Event"),
    path('Enroll_Event/<str:pk>/',views.Enroll_Event,name="Enroll_Event"),
    path('Search_Profile/',views.search_profiles,name="Search_Profile"),
    path('Change_user_status/<str:pk>/',views.change_user_status,name="user_change_status"),
    

]
