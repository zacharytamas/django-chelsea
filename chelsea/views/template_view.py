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
        self.context_add('request', request)

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

    def context(self):
        return self.template_context

    def context_add(self, key, value):
        """Given a key and a value, adds it to the template context."""
        self.template_context[key] = value

    def context_remove(self, key):
        if key in self.template_context:
            del self.template_context[key]
            return True
        else:
            return False

    def context_update(self, key, value):
        """Given a key and value, update the context."""
        # TODO Implement.

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
                raise Exception('ZView: No configured template_name to render.')

        if context is None:
            context = self.context()

        if 'request' in context:
            return django_render_to_response(template_name, context,
                context_instance=RequestContext(context['request']))
        else:
            return django_render_to_response(template_name, context)

    render = render_to_response  # a shortcut

    # The default GET behavior is to just render the template
    # without doing any specific logic.
    def get(self, request, *args, **kwargs):
        pass
