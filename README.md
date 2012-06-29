# Chelsea Django framework

Chelsea is a web framework for a web framework. Chelsea is the work of 
one developer, [Zachary Jones](http://www.zacharytamas.com/), and is 
the result of an effort to abstract and simplify repetitive development 
he found himself doing time and time again.

## Basic Usage

Chelsea currently has three different classes for you to use: `CView`, 
`CTemplateView`, and `CFormView`. The most common usage of Chelsea is 
the `CTemplateView`, which lets you easily respond to, render to HTML, and 
return an HttpResponse. To best demonstrate how `CTemplateView` helps you, 
let's compare the same view before and after:

    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from django.contrib import messages
    from django.contrib.auth.decorators import login_required
    from myproject.apps.blog.models import Post
    
    @login_required
    def delete_post(request, post_id):
        """Demo view."""
        
        if request.method == "POST":
            post = Post.objects.get(id=post_id)
            
            if request.user is not post.author:
                messages.warning(request, "You cannot delete a post you don't own!")
                return HttpResponseRedirect('/')
            
            post.delete()
            
            context = {
                'post': post
            }
            messages.success(request, "Successfully removed '%s'" % post.title)
            
            return render_to_response(
                'blog/delete_post.html', 
                context, 
                context_instance=RequestContext(request)
            )
        else:
            post = Post.objects.get(id=post_id)
            context = {
                'post': post
            }
            
            return render_to_response(
                'blog/delete_post.html', 
                context, 
                context_instance=RequestContext(request)
            )

Now let's do it using Chelsea:

    from chelsea.views import CTemplateView
    from myproject.apps.blog.models import Post
    
    class DeletePostView(CTemplateView):
        """Demo view."""
        
        template_name = "blog/delete_post.html"
        login_required = True
        
        def get(self, request, post_id):
            post = Post.objects.get(id=post_id)
            self.context_add(post=post)
        
        def post(self, request, post_id):
            post = Post.objects.get(id=post_id)
            if request.user is not post.author:
                self.msg_warning("You cannot delete a post you don't own!")
                self.redirect_to("/")  # this accepts URL, path, or URL name
            post.delete()
            self.context_add(post=post)
            self.msg_success("Successfully removed '%s'" % post.title)

So much easier! Here are a few important points:

* The class will redirect HTTP requests to the method on the 
  class named for the HTTP method: e.g. GET = get(), POST = post()
* If your method does not return an HttpResponse, the class will 
  render it for you automatically.
* Common tasks like requiring a user to be logged in, using Django's 
  messages framework, and returning redirects are included in the 
  class and so you do not have to import them yourself.

## Using CFormView

Another helpful usage of Chelsea is the `CFormView` which handles 
views which implement form functions. It extends `CTemplateView`, so 
all the previous functionality is available.

Without Chelsea:

    from django.contrib import messages
    from django.contrib.auth.models import User
    from django.contrib.auth.decorators import login_required
    from django.core.urlresolvers import reverse
    from django.http import HttpResponse, HttpResponseRedirect
    from django.shortcuts import render_to_response, get_object_or_404
    from django.template import RequestContext
    from django.template.defaultfilters import slugify
    
    from myproject.apps.plugins.models import (Release, Plugin)
    from myproject.apps.plugins.forms import ReleaseForm
    
    @login_required
    def release_add(request, username, slug):
        """Demo view."""
        
        user = User.objects.get(username=username)
        plugin = Plugin.objects.get(slug=slug)
        
        if request.user != plugin.author:
            messages.warning(request, "You cannot add releases to 
                plugins you aren't the author of.")
            return HttpResponseRedirect(reverse("plugins_list"))
        
        if request.method == "POST":
            form = ReleaseForm(request.POST, request.FILES)
            if form.is_valid():
                release = form.save(commit=False)
                release.slug = slugify(release.name)
                form.save()
                messages.success(request, "Successfully created your release.")
                return HttpResponseRedirect(
                    reverse("plugin_detail", args=[plugin.slug]))
        else:
            form = ReleaseForm()
        
        context = {
            'plugin': plugin,
            'form': form
        }
        return render_to_response('plugins/release_add.html', context,
            context_instance=RequestContext(request))

Now with Chelsea:

    from django.contrib.auth.models import User
    from chelsea.views import CFormView
    
    from myproject.apps.plugins.forms import ReleaseForm
    from myproject.apps.plugins.models import (Plugin, Release)
    
    class ReleaseAddView(CFormView):
        """Demo view."""
        
        template_name = "plugins/release_add.html"
        login_required = True
        form_class = ReleaseForm
        
        def form_will_be_created(self):
            self.user = User.objects.get(username=username)
            self.plugin = Plugin.objects.get(slug=slug)
            self.context_add(user=self.user, plugin=self.plugin)

            if request.user != self.plugin.author:
                self.msg_warning("You cannot add releases to 
                    plugins you aren't the author of.")
                self.redirect_to("plugins_list")
        
        def form_was_validated(self, form, data):
            release = form.save(commit=False)
            release.slug = slugify(release.name)
            form.save()
            self.msg_success("Successfully created your release.")
            self.redirect_to("plugin_detail", args=[plugin.slug])
        
