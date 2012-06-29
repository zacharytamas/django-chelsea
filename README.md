# Chelsea Django framework

Chelsea is a web framework for a web framework. Chelsea is the work of 
one developer, [Zachary Jones](http://www.zacharytamas.com/), and is 
the result of an effort to abstract and simplify repetitive development 
he found himself doing time and time again.

Chelsea consists of Django class-based views which abstracts away many 
of the repetitive tasks in Django view and template rendering processes. 
Chelsea is very extensible by design and makes your code "read" a lot 
better while only requiring you to write the logic specific to your 
view and taking care of the common request-render-response cycle 
functions for you.

## Basic Usage

Chelsea currently has three different classes for you to use: `CView`, 
`CTemplateView`, and `CFormView`. The most common usage of Chelsea is 
the `CTemplateView`, which lets you easily respond to, render, and 
return an HttpResponse. To best demonstrate how `CTemplateView` helps you, 
let's compare the same view before and after:

    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from django.contrib import messages
    from myproject.apps.blog.models import Post
    
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
        automaps = {'post': Post}
        
        def get(self, request, post):
            self.context_add(post=post)
        
        def post(self, request, post):
            
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
* If you provide an "automap" entry for a Model, Chelsea will 
  automatically query for it for you and pass it to your method. 
  In this case, Django passes "post_id" from the URL schema as 
  a primary key of Post, and Chelsea grabs it for you and passes 
  it to your view so you don't have to. If you don't define an 
  automap this magic doesn't happen.
