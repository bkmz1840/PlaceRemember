from django.test import TestCase
from django.urls.exceptions import NoReverseMatch
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from myPlaceRemember.models import *


class TestMyPlaceRemember(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_name = "Test"
        cls.user_password = "1234"
        cls.avatar = "https://picture.com/1.png"
        cls.user = User.objects.create_user(cls.user_name, "example@mail.ru",
                                            cls.user_password)
        Profile.objects.create(user=cls.user, avatar=cls.avatar)

    def test_should_redirect_to_login_for_not_auth_user(self):
        client = self.client
        url = "/myPlaceRemember/"
        self.assertRaises(NoReverseMatch, client.get, url)
        client.login(username=self.user_name, password=self.user_password)
        ans = client.get(url)
        good_templates = ["myPlaceRemember/index.html", "layout.html",
                          "myPlaceRemember/header.html"]
        self.assertListEqual(
            list(map(lambda t: t.name, ans.templates)),
            good_templates
        )

    def test_should_to_slug_from_title_work_right(self):
        title_1 = "Бразилия"
        title_2 = "Выходные в Германии"
        title_3 = "@?/$%Россия"
        title_4 = "Test Text"
        self.assertEqual(f"{self.user_name}-Braziliya",
                         to_slug_from_title(title_1, self.user_name))
        self.assertEqual(f"{self.user_name}-Vyhodnye_v_Germanii",
                         to_slug_from_title(title_2, self.user_name))
        self.assertEqual(f"{self.user_name}-Rossiya",
                         to_slug_from_title(title_3, self.user_name))
        self.assertEqual(f"{self.user_name}-Test_Text",
                         to_slug_from_title(title_4, self.user_name))

    def test_should_create_remember_right(self):
        profile = Profile.objects.get(user=self.user)
        title = "Россия"
        remember = RememberModel.objects.create(
            title=title, body="Big text", profile=profile,
            location="Россия, Москва")
        self.assertEqual(f"{profile.user.username}-Rossiya",
                         remember.slug)
        self.assertEqual(title, str(remember))

    def test_should_get_urls_work_right(self):
        profile = Profile.objects.get(user=self.user)
        title = "Отдых"
        remember = RememberModel.objects.create(
            title=title, body="Big text", profile=profile,
            location="Россия, Москва")
        right_slug = f"{profile.user.username}-Otdyh"
        self.assertEqual(f"/myPlaceRemember/{right_slug}/",
                         remember.get_absolute_url())
        self.assertEqual(f"/myPlaceRemember/{right_slug}/edit/",
                         remember.get_absolute_update_url())
        self.assertEqual(f"/myPlaceRemember/{right_slug}/del/",
                         remember.get_absolute_delete_url())

    def test_should_create_remember_if_form_valid(self):
        client = self.client
        client.login(username=self.user_name, password=self.user_password)
        title = "Отдых"
        ans = client.post("/myPlaceRemember/create/", {
            "title": title,
            "location": 'Россия, Москва',
            "body": "Some big text"
        })
        self.assertEqual("/myPlaceRemember/", ans.url)
        self.assertIsNotNone(RememberModel.objects.get(title=title))
        self.assertEqual("/myPlaceRemember/", ans.url)
        ans = client.post("/myPlaceRemember/create/")
        template_create_remember = "myPlaceRemember/create_remember.html"
        self.assertIn(template_create_remember,
                      list(map(lambda t: t.name, ans.templates)))

    def test_should_update_remember(self):
        client = self.client
        client.login(username=self.user_name, password=self.user_password)
        profile = Profile.objects.get(user=self.user)
        new_title = "Россия"
        new_location = "Россия, Москва"
        remember = RememberModel.objects.create(title="Отдых",
                                                location="Германия, Берлин",
                                                body="Text", profile=profile)
        ans = client.post(f"/myPlaceRemember/{remember.slug}/edit/", {
            'title': new_title, "location": new_location
        })
        self.assertIsNotNone(RememberModel.objects.get(title=new_title))
        new_remember = RememberModel.objects.get(title=new_title)
        self.assertEqual(f"{profile.user.username}-Rossiya", new_remember.slug)
        self.assertEqual(new_location, new_remember.location)
        new_slug = new_remember.slug
        self.assertEqual(f"/myPlaceRemember/{new_slug}/", ans.url)
        ans = client.post(f"/myPlaceRemember/{new_slug}/edit/")
        template_edit_remember = "myPlaceRemember/update_remember.html"
        self.assertIn(template_edit_remember,
                      list(map(lambda t: t.name, ans.templates)))

    def test_should_remove_remember(self):
        client = self.client
        client.login(username=self.user_name, password=self.user_password)
        profile = Profile.objects.get(user=self.user)
        title = "TestTitle"
        remember = RememberModel.objects.create(title=title, location="Россия, Москва",
                                                body="Some body", profile=profile)
        ans = client.get(f"/myPlaceRemember/{remember.slug}/del/")
        self.assertRaises(ObjectDoesNotExist, RememberModel.objects.get, title=title)
        self.assertEqual("/myPlaceRemember/", ans.url)

    def test_should_return_right_temples_when_open_remember_detail(self):
        right_templates = ["myPlaceRemember/remember_detail.html", "layout.html",
                           "myPlaceRemember/header.html"]
        client = self.client
        client.login(username=self.user_name, password=self.user_password)
        profile = Profile.objects.get(user=self.user)
        remember = RememberModel.objects.create(title="Test", location="Россия, Москва",
                                                body="Some body", profile=profile)
        ans = client.get(f"/myPlaceRemember/{remember.slug}/")
        self.assertListEqual(
            list(map(lambda t: t.name, ans.templates)),
            right_templates)
