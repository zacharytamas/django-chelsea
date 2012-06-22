import sys

from django.http import HttpResponse
from django.shortcuts import render_to_response as django_render_to_response
from django.template import RequestContext

from view import CView

class CTemplateView(CView):
    """A view which revolves around returning HttpResponses that
    are rendered from HTML templates."""

    ################################################################
    # Low-level view dispatching
    ################################################################

    def dispatch(self, request, *args, **kwargs):

        # Automatically add the request object to the
        # template context.
        self.context_add('request')

        response = super(CTemplateView, self).dispatch(request, *args, **kwargs)

        if isinstance(response, HttpResponse):
            return response

        # the view did not return a Response, let's automatically
        # render for them as a convenience.
        else:
            return self.render()

    ################################################################
    # Template context methods
    ################################################################

    template_context = {}

    def context(self, key=None):
        if key is None:
            return self.template_context
        else:
            return self.template_context[key]

    def context_add(self, *args, **kwargs):
        """Adds variables to the template context."""

        if len(args):
            # TODO insert test for frame support
            caller_context = sys._getframe(1).f_locals
            for arg in args:
                if type(arg) in [str, unicode]:
                    try:
                        self.template_context[arg] = caller_context[arg]
                    except:
                        raise Exception('CTemplateView: "%s" variable not found in view context.' % arg)
                else:
                    raise Exception('CTemplateView: Could not map template context variables.')

        if len(kwargs):
            for k,v in kwargs.iteritems():
                self.template_context[k] = v

    def context_remove(self, key):
        if key in self.template_context:
            del self.template_context[key]
            return True
        else:
            return False

    def context_update(self, key, value):
        """Given a key and value, update the context."""
        if key in self.template_context:
          self.template_context[key] = value
          return True
        else:
          return False

    def context_integrate(self, dictionary):
        """Given a dictionary, integrates it into the 
        template context."""
        # TODO Implement.

    ################################################################
    # Template rendering methods
    ################################################################

    template_name = None

    def render_to_response(self, context=None, template_name=None):
        """Renders a response using the current tempalte context."""

        if template_name is None:
            if self.template_name is not None:
                template_name = self.template_name
            else:
                raise Exception('CView: No configured template_name'
                    ' to render.')

        if context is None:
            context = self.context()

        if 'request' in context:
            return django_render_to_response(template_name, context,
                context_instance=RequestContext(context['request']))
        else:
            return django_render_to_response(template_name, context)

    render = render_to_response  # a shortcut

    def get(self, request, *args, **kwargs):
        """The default GET behavior is to just render the
        template without doing any specific logic."""
        pass
    
    post = get  # by default POST hits run the GET method
