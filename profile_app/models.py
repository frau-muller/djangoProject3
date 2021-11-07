import bcrypt
from django.db import models
from login_app.models import User  
from django_random_queryset import RandomManager

class CommentManager(models.Manager):
    def validateEmptyComment(self, post_data): 
        errors={}
        if post_data['comment'] == '' :
            errors['comment']='Please fill in the field. You can not submit an empty comment'
        return errors

    def validateEmptyReply(self, post_data): 
        errors={}
        if post_data['reply'] == '' :
            errors='Please fill in the field. You can not submit an empty reply'
        return errors

class Comment(models.Model):
    comment_content = models.TextField()
    user_comment = models.ForeignKey(User, related_name='comment_by', on_delete=models.CASCADE)   
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    #reply_to_comment = a list of replies to a specific comment   FROM reply

    objects = CommentManager()

    def __repr__(self):
        return f'<Comment object: ID:{self.id} Content:{self.comment_content} By:{self.user_comment}>'

class Reply(models.Model):
    reply_content = models.TextField()
    user_reply = models.ForeignKey(User, related_name='reply_by', on_delete=models.CASCADE)  
    reply_to = models.ForeignKey(Comment, related_name='reply_to_comment', on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __repr__(self):
        return f'<Reply object: ID:{self.id} Content:{self.reply_content} By:{self.user_reply} Reply To={self.reply_to}>'