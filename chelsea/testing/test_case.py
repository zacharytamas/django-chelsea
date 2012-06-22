from django.test import TestCase
from django.conf import settings

class CTestCase(TestCase):
    """A Chelsea Test Case."""
    
    auth_credentials = []
    
    ################################################################
    # Extra assertions
    ################################################################

    def assertRequiresAuthentication(self, url_name, args=[]):
        """Asserts that a view at a given URL name requires
           authentication to be accessed."""
        url = self.__determine_url(url_name, args=args)
        r = self.client.get(url)
        self.assertRedirects(r, '%s?next=%s' % (settings.LOGIN_URL, url))
    
    def assertDoesNotRequireAuthentication(self, url_name, args=[]):
        """Asserts that a view at a given URL name does not
        require authentication to be accessed."""
        try:
            self.assertRequiresAuthentication(url_name, args)
            passed = False
        except:
            passed = True
        
        if not passed:
            raise Exception('View required authentication, expected it to not.')
    
    def assertStatusCodeForURL(self, url_name, status_code=200, args=[]):
        """Asserts that a given url_name's view returns a given status code."""
        url = self.__determine_url(url_name, args)
        r = self.client.get(url)
        self.assertStatusCodeForResponse(r, status_code)

    def assertStatusCodeForResponse(self, resp, status_code=200):
        """Asserts that a given response's status code matches a given one."""
        self.assertEqual(resp.status_code, status_code)

    def assertInContext(self, resp, key):
        """Asserts that a given key is available in the response's context."""
        self.assertTrue(key in resp.context)

    def assertInitialFormFieldValue(self, form, field, value):
        """Asserts that the initial value of a field on a given form
        equals a given value."""
        self.assertEqual(form.initial[field], value)

    def login(self, username=None, password=None):
        """Login to the client using the instance's `auth_credentials`."""
        if (username is not None and password is not None):
            a = [username, password]
        elif (username is not None and password is None):
            a = [username, "testcase"]
        elif len(self.auth_credentials) == 2:
            a = self.auth_credentials
        else:
            return False
        return self.client.login(username=a[0], password=a[1])

    def __determine_url(self, url, args=[]):
        """Determines a URL given a name. If the given URL is actually
        a path it just echoes it back."""
        if(url.startswith("/")):
            return url
        return reverse(url, args=args)
