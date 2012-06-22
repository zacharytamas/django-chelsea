from chelsea.views import CView
from chelsea.views import CTemplateView

################################################################
# CView
################################################################

class TestCViewLoginRequired(CView):
    """Tests the login required views."""
    login_required = True

################################################################
# CTemplateView
################################################################

class TestTemplateRenderView(CTemplateView):
    """Tests that a view renders."""
    template_name = "tests/basic.html"

class TestTemplateRenderOverride(TestTemplateRenderView):
    pass
