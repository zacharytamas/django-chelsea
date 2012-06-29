from django.forms import Form

from chelsea.views import CTemplateView

class CFormView(CTemplateView):
    """A view which handles typical form processes."""

    form_class = None

    def __init__(self):
        if not isinstance(self.form_class, Form):
            raise Exception('CFormView: form_class must be a subclass of Form')
        super(CFormView, self).__init__()

    def get(self, request, *args, **kwargs):
        
        self.form_will_be_created()
        form = self.create_form()
        self.form_was_created(form)

        self.view_will_render()
        self.context_add(form=form)

    def post(self, request, *args, **kwargs):
        
        self.form_will_be_created()
        form = self.create_form(request.POST, request.FILES)
        self.form_was_created(form)

        self.form_will_attempt_validation(form)
        valid = form.is_valid()

        if valid:
            self.form_was_validated(form, form.cleaned_data)
        else:
            self.form_was_invalid(form)

        self.view_will_render()
        self.context_add(form=form)

    def create_form(self, *args, **kwargs):
        """Creates and returns a form."""
        form = self.form_class(*args, **kwargs)
        return form
    
    ################################################################
    # Cocoa-style Events to be overriden to specify functionality.
    ################################################################

    def form_will_be_created(self):
        """Called directly before a form is created."""
        pass

    def form_was_created(self, form):
        """Called after a form is created and is
        passed the new form."""
        pass

    def form_will_attempt_validation(self, form):
        """Called directly before a form will attempt to
        validate and receives a reference to the form."""
        pass

    def form_was_validated(self, form, data):
        """Called when a form has successfully validated 
        and receives a reference to the form and a
        dictionary containing its cleaned data."""
        pass

    def form_was_invalid(self, form):
        """Called when a form was unsuccessful in validation
        and receives a reference to the form."""
        pass

    def view_will_render(self):
        """Called directly before the view will
        attempt to render itself."""
        pass


