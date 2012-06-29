from django.contrib.auth.models import User

from chelsea.views import CView
from chelsea.views import CTemplateView

################################################################
# CView
################################################################

class TestCViewLoginRequired(CView):
    """Tests the login required views."""
    login_required = True

class TestCViewAutoMaps(CView):
    """"""
    automaps = {'user': User}
    def get(self, request, user):
        print user.username

################################################################
# CTemplateView
################################################################

class TestTemplateRenderView(CTemplateView):
    """Tests that a view renders."""
    template_name = "tests/basic.html"

class TestTemplateRenderOverride(TestTemplateRenderView):
    pass
