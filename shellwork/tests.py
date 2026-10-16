import json
import shutil
import tempfile

from django.core.management import call_command
from django.test import TestCase, override_settings

from .models import Breed, BreedingPairing, Citation, Photo


TMP_MEDIA = tempfile.mkdtemp(prefix="shellwork-test-media-")


@override_settings(MEDIA_ROOT=TMP_MEDIA)
class ShellworkTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("load_shellwork", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TMP_MEDIA, ignore_errors=True)

    def test_seed_loaded(self):
        self.assertEqual(Breed.objects.count(), 17)
        self.assertTrue(Photo.objects.filter(kind="egg").exists())
        self.assertTrue(BreedingPairing.objects.exists())
        for b in Breed.objects.all():  # every breed is backed by at least one source
            self.assertTrue(Citation.objects.filter(breed=b).exists(), b.slug)

    def test_public_pages(self):
        for url in ["/shellwork/", "/shellwork/breed/welsummer/", "/shellwork/breed-for-a-colour/?colour=green",
                    "/shellwork/compare/?b=marans,welsummer", "/shellwork/glossary/", "/shellwork/sources/",
                    "/shellwork/offline/", "/shellwork/manifest.webmanifest", "/shellwork/sw.js"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_root_redirects_to_shellwork(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], "/shellwork/")

    def test_everything_under_shellwork(self):
        html = self.client.get("/shellwork/breed/welsummer/").content.decode()
        self.assertIn("/shellwork/static/shellwork/css/", html)
        self.assertIn("/shellwork/media/", html)
        self.assertNotIn('"/static/', html)
        self.assertNotIn('"/media/', html)
        m = json.loads(self.client.get("/shellwork/manifest.webmanifest").content)
        self.assertEqual(m["scope"], "/shellwork/")
        self.assertTrue(all(i["src"].startswith("/shellwork/static/") for i in m["icons"]))
        sw = self.client.get("/shellwork/sw.js")
        self.assertEqual(sw["Service-Worker-Allowed"], "/shellwork/")
        self.assertIn('"/shellwork/static/shellwork/js/rolodex.js"', sw.content.decode())

    def test_admin_registered(self):
        from django.contrib import admin
        for model in (Breed, Citation, Photo, BreedingPairing):
            self.assertIn(model, admin.site._registry)
