from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
# from django.template.defaultfilters import slugify


class Image(models.Model):
    image = models.ImageField(upload_to='images/',default='1')
    name = models.CharField(max_length =30)
    caption = models.CharField(max_length =30)
    profile = models.ForeignKey(User,on_delete=models.CASCADE,default='0')
    likes= models.ManyToManyField(User, related_name='image_like')
    comments = models.CharField(max_length =30)
    
    def __str__(self):
        return f'{self.profile.username}\'s Image- {self.name}'
    class Meta:
        ordering = ['name']
        
    def save_image(self):
        self.save()
    def number_of_likes(self):
        return self.likes.count()
    def delete_image(self):
        self.delete()
    @classmethod
    def update_image(cls,old,new):
        cap = Image.objects.filter(caption=old).update(caption=new)
        return cap
    @classmethod
    def search_by_name(cls, image):
        images = cls.objects.filter(image__icontains=image)
        return images
class Preference(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,default='0')
    post= models.ForeignKey(Image,on_delete=models.CASCADE,default='0')
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)

    
    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")

class Profile(models.Model):
    bio = models.CharField(max_length =30)
    profile_photo = models.ImageField(upload_to ='images/',default='1')
    name = models.CharField(blank=True, max_length=120)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',null=True)
    
    def __str__(self):
        return self.name
    @classmethod
    def profile(cls):
        profiles = cls.objects.all()
        return profiles
    def delete_profile(self):
        self.delete()
    def photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url

    def save_profile(self):
        self.user
    def update_profile(cls,old,new):
        bio = Profile.objects.filter(bio=old).update(bio=new)
        return bio
    def __str__(self):
        return self.name

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     try:
    #         instance.Profile.save()
    #     except ObjectDoesNotExist:
    #         Profile.objects.create(user=instance)
class NewsLetterRecipients(models.Model):
    is_email_verified = models.BooleanField(default=False)
    name = models.CharField(max_length = 30)
    email = models.EmailField()


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey('Profile',on_delete=models.CASCADE,related_name='comment')
    photo = models.ForeignKey('Image',on_delete=models.CASCADE,related_name='comment')

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return f'{self.user.name} Image'
    def save_comment(self):
        self.comment 
    
class Follow(models.Model):
    follower = models.CharField(max_length=50)
    user = models.CharField(max_length=50)

    def __str__(self):
        return self.user
