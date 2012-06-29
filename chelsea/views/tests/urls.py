from django.conf.urls import patterns, include, url

from views import (
    # CView views
    TestCViewLoginRequired,
    
    # CTemplateView views
    TestTemplateRenderView,
)

urlpatterns = patterns('',

    # CView views
    
    url(r'^cview/test_login_required/$', TestCViewLoginRequired.as_view(),
        name='cview/test-login-required'),
    url(r'^cview/test_automaps/(?P<user_id>)/$', TestCViewAutoMaps.as_view(),
        name='cview/test-automaps'),
    
    # CTemplateView views
    
    url(r'^template_render_view/$', TestTemplateRenderView.as_view(), 
        name='test-template-render-view'),
    
    # Auth views
    
    url(r'accounts/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'blank.html'}),

)
