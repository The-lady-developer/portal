from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView)
from django.views.generic.detail import SingleObjectMixin
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from common.mixins import UserDetailsMixin
from community.mixins import CommunityMenuMixin
from community.models import Community
from blog.forms import AddNewsForm, EditNewsForm, AddResourceForm
from blog.models import News, Resource


class CommunityNewsListView(UserDetailsMixin, CommunityMenuMixin,
                            SingleObjectMixin, ListView):
    """List of Community news view"""
    template_name = "blog/post_list.html"
    page_slug = 'news'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Community.objects.all())
        return super(CommunityNewsListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add Community object under different name and type of post."""
        context = super(CommunityNewsListView, self).get_context_data(**kwargs)
        context["community"] = self.object
        context["post_type"] = "news"
        return context

    def get_queryset(self):
        return News.objects.filter(community=self.object)

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object


class CommunityNewsView(UserDetailsMixin, CommunityMenuMixin, DetailView):
    """Single News Community view"""
    template_name = "blog/post.html"
    model = Community
    page_slug = 'news'

    def get_context_data(self, **kwargs):
        """Add Community object, News object and post type to the context"""
        context = super(CommunityNewsView, self).get_context_data(**kwargs)
        context["community"] = self.object

        news_slug = self.kwargs['news_slug']
        context['post'] = get_object_or_404(News, slug=news_slug)
        context["post_type"] = "news"
        return context

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object


class AddCommunityNewsView(LoginRequiredMixin, PermissionRequiredMixin,
                           CreateView):
    """Add News to a Community view"""
    template_name = "blog/add_post.html"
    model = News
    form_class = AddNewsForm
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_news",
                       kwargs={"slug": self.community.slug,
                               "news_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Community object and post type to the context"""
        context = super(AddCommunityNewsView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        context['post_type'] = 'news'
        return context

    def get_form_kwargs(self):
        """Add request user and community object to the form kwargs.
        Used to autofill form fields with author and community without
        explicitly filling them up in the form."""
        kwargs = super(AddCommunityNewsView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        kwargs.update({'community': self.community})
        return kwargs

    def check_permissions(self, request):
        """Check if the request user has the permissions to add new community
        news. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("add_community_news", self.community)


class EditCommunityNewsView(LoginRequiredMixin, PermissionRequiredMixin,
                            UpdateView):
    """Edit existing Community News view"""
    template_name = "blog/edit_post.html"
    model = News
    slug_url_kwarg = "news_slug"
    form_class = EditNewsForm
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_news",
                       kwargs={"slug": self.community.slug,
                               "news_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Community object to the context"""
        context = super(EditCommunityNewsView, self).get_context_data(**kwargs)
        context['community'] = self.community
        return context

    def check_permissions(self, request):
        """Check if the request user has the permissions to edit community
        news. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("change_community_news", self.community)


class DeleteCommunityNewsView(LoginRequiredMixin, PermissionRequiredMixin,
                              DeleteView):
    """Delete existing Community News view"""
    template_name = "blog/post_confirm_delete.html"
    model = News
    slug_url_kwarg = "news_slug"
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful deletion"""
        return reverse("view_community_news_list",
                       kwargs={"slug": self.community.slug})

    def get_context_data(self, **kwargs):
        """Add Community object to the context"""
        context = super(DeleteCommunityNewsView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        context['post_type'] = 'news'
        return context

    def check_permissions(self, request):
        """Check if the request user has the permissions to delete community
        news. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("delete_community_news", self.community)


class CommunityResourceListView(UserDetailsMixin, CommunityMenuMixin,
                                SingleObjectMixin, ListView):
    """List of Community resources view"""
    template_name = "blog/post_list.html"
    page_slug = 'resources'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Community.objects.all())
        return super(CommunityResourceListView, self).get(request, *args,
                                                          **kwargs)

    def get_context_data(self, **kwargs):
        """Add Community object under different name and type of post."""
        context = super(CommunityResourceListView, self).get_context_data(
            **kwargs)
        context["community"] = self.object
        context["post_type"] = "resource"
        return context

    def get_queryset(self):
        return Resource.objects.filter(community=self.object)

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object


class CommunityResourceView(UserDetailsMixin, CommunityMenuMixin, DetailView):
    """Resource Community view"""
    template_name = "blog/post.html"
    model = Community
    page_slug = 'resources'

    def get_context_data(self, **kwargs):
        """Add Community object, Resource object and post type to the
        context"""
        context = super(CommunityResourceView, self).get_context_data(**kwargs)
        context["community"] = self.object

        resource_slug = self.kwargs['resource_slug']
        context["post"] = get_object_or_404(Resource, slug=resource_slug)
        context["post_type"] = "resource"
        return context

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object


class AddCommunityResourceView(LoginRequiredMixin, PermissionRequiredMixin,
                               CreateView):
    """Add News to a Community view"""
    template_name = "blog/add_post.html"
    model = Resource
    form_class = AddResourceForm
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_resource",
                       kwargs={"slug": self.community.slug,
                               "resource_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Community object and post type to the context"""
        context = super(AddCommunityResourceView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        context['post_type'] = 'resource'
        return context

    def get_form_kwargs(self):
        """Add request user and community object to the form kwargs.
        Used to autofill form fields with author and community without
        explicitly filling them up in the form."""
        kwargs = super(AddCommunityResourceView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        kwargs.update({'community': self.community})
        return kwargs

    def check_permissions(self, request):
        """Check if the request user has the permissions to add new community
        news. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("add_community_resource", self.community)
