from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import View

class CView(View):
    """A Chelsea View."""

    login_required = False
    user_passes_test = None
    user_in_group = None

    ################################################################
    # Low-level view dispatching
    ################################################################

    def get_view(self, request, *args, **kwargs):
        """Determines and returns the view needed for the 
        given request."""

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), 
                self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        return handler

    def dispatch(self, request, *args, **kwargs):
        """Handles the dispatching of view requests."""

        view = self.get_view(request, *args, **kwargs)

        # "Requires login" functionality.
        # TODO rewrite?
        if self.login_required is not False:
            if self.login_required is True:
                view = login_required(view)
            elif isinstance(self.login_required, list):
                if request.method.lower() in self.login_required:
                    view = login_required(view)

        if request.method.lower() in self.login_required:
            view = login_required(view)

        # If there is a specified test method, test the
        # user against the method.
        if self.user_passes_test is not None:
            result = self.user_passes_test(request.user)
            if not result:
                return self.render_redirect("/")

        # TODO Implement the user_in_group restrictions.
        # if self.user_in_group is not None:
        #     if type(self.user_in_group) in [str, unicode]:
        #         self.user_in_group = [self.user_in_group]

        self.request = request
        self.args = args
        self.kwargs = kwargs
        return view(request, *args, **kwargs)

    ################################################################
    # Response returns
    ################################################################

    def redirectTo(self, to, *args, **kwargs):
        """Returns a redirect to the given URL."""

        response = redirect(to, *args, **kwargs)

        # By default, raise a redirect, which will cause the view
        # processing to stop and return this redirect.
        if kwargs.pop("raise", True):
            raise response
        else:
            return response
