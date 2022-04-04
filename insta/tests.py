from django.test import TestCase
from .models import Image, Profile
from django.contrib.auth.models import User


# Create your tests here.
class ImageTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.profile = Profile(user=Profile(name='mercy'))
        self.profile.user.save()
        self.profile.save()
        self.image = Image(user=self.profile,image='download.jpeg', name='pillaar', caption='shanghai')
        self.image.save_image()
        
    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))
        self.assertTrue(isinstance(self.image, Image))     # Testing Save Method
    def test_save_image(self):
        self.image.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images) > 0)
    def tearDown(self):
        Profile.objects.all().delete()
        Image.objects.all().delete()
    def test_update_image_caption(self):
        self.image.save_image()
        new_caption =Image.update_image('shangai','norway')
        image = Image.objects.get(caption='norway')
        self.assertEqual(image.caption,'norway')
    
class ProfileTestClass(TestCase):
    def setUp(self):
        self.user = Profile(name='mercy')
        self.user.save()
        self.profile = Profile(id=1,user=self.user,photo='download.jpeg',bio='Sofatware Dev', name='Mercy')
        self.profile.save_profile()

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
        Image.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.user,User))
        self.assertTrue(isinstance(self.profile, Profile))

    def test_save_method(self):
        self.profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile) > 0)