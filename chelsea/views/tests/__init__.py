from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from chelsea.views import (CView, CTemplateView)
from chelsea.testing import CTestCase
from chelsea.views.tests.views import TestCViewAutoMaps

class CViewTestCases(CTestCase):
    """Tests for the CView class."""
    
    urls = 'chelsea.views.tests.urls'
    
    auth_credentials = ["zachary", "testcase"]
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="zachary", password="testcase")
    
    ################################################################
    # Utilities
    ################################################################
    
    

    ################################################################
    # Tests as view
    ################################################################
    
    def test_login_required(self):
        """Tests the login_required property of a view."""
        url = reverse("cview/test-login-required")
        
        # Should redirect because I am not logged in.
        self.assertRequiresAuthentication(url)
        
        # Login and then assert login isn't required anymore
        self.login()
        self.assertDoesNotRequireAuthentication(url)

    ################################################################
    # Tests as class
    ################################################################
    
    def test_view_instance(self):
        """Tests the CView."""
        pass


class CTemplateViewTestCases(CTestCase):
    """Tests for the CTemplateView."""
    
    urls = 'chelsea.views.tests.urls'
    
    def test_template_render_view(self):
        url = reverse("test-template-render-view")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
