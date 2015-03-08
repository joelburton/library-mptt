from django.test import TestCase

from .models import Folder, Document


class LibraryTestCase(TestCase):
    fixtures = ['sample.json']

    def test_change_folder_slug_updates_paths(self):
        # test that renaming folder slugs fixes all of the items below

        # get a sample series of folders & docs
        js = Folder.objects.get(slug='javascript')
        js_overview = Document.objects.get(slug='overview', folder=js)
        routing = Folder.objects.get(slug='routing')
        routing_ex = Document.objects.get(slug='routing-example')

        # sanity checking that fixtures loaded and to help differentiate from the expected
        # change, below
        self.assertEqual(js.path, 'javascript')
        self.assertEqual(js_overview.path, 'javascript/overview')
        self.assertEqual(routing.path, 'javascript/angular/routing')
        self.assertEqual(routing_ex.path, 'javascript/angular/routing/routing-example')

        # rename the javascript folder, which should trigger a rename of everything below this
        js.slug = "js"
        js.save()

        # get objects again from db, since they will have changed under us
        js_overview = Document.objects.get(slug='overview', folder=js)
        routing = Folder.objects.get(slug='routing')
        routing_ex = Document.objects.get(slug='routing-example')

        # check that the paths have updated javascript->js
        self.assertEqual(js.path, 'js')
        self.assertEqual(js_overview.path, 'js/overview')
        self.assertEqual(routing.path, 'js/angular/routing')
        self.assertEqual(routing_ex.path, 'js/angular/routing/routing-example')

    def test_change_doc_slug_updates_path(self):
        # test that renaming a doc fixes up path

        routing_ex = Document.objects.get(slug='routing-example')
        routing_ex.slug = 'example'
        routing_ex.save()

        self.assertEqual(routing_ex.path, 'javascript/angular/routing/example')


class LibraryViewsTestCase(TestCase):
    fixtures = ['sample.json']

    def test_traversal(self):
        response = self.client.get('/library/javascript/')
        self.assertContains(response, "<h1>Javascript</h1>")

        response = self.client.get('/library/javascript/angular/')
        self.assertContains(response, "<h1>Angular</h1>")

        response = self.client.get('/library/javascript/angular', follow=True)
        self.assertContains(response, "<h1>Angular</h1>")

        response = self.client.get('/library/javascript/angular/routing/routing-example/')
        self.assertContains(response, "<h1>Routing Example</h1>")

        response = self.client.get('/library/javascript/angular/routing/routing-example',
                                   follow=True)
        self.assertContains(response, "<h1>Routing Example</h1>")

    def test_traversal_fail(self):
        response = self.client.get('/library/not-found/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/library/not-found', follow=True)
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/library/javascript/angular/not-found/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/library/javascript/angular/not-found', follow=True)
        self.assertEqual(response.status_code, 404)
