"""
    仅用于 django管理后台开发
"""
from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.admin.options import *
from utils.lock import CacheLock
from meeting.models import Meeting, MeetingRoom
from meeting.forms import MeetingForm, MeetingRoomForm


class MeetRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'status', 'create_time', 'update_time')
    list_per_page = 20
    form = MeetingRoomForm


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'room', 'time_begin', 'time_end', 'is_active')
    list_per_page = 20
    form = MeetingForm

    def _changeform_view(self, request, object_id, form_url, extra_context):
        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField(
                "The field %s cannot be referenced." % to_field
            )

        model = self.model
        opts = model._meta

        if request.method == "POST" and "_saveasnew" in request.POST:
            object_id = None

        add = object_id is None

        if add:
            if not self.has_add_permission(request):
                raise PermissionDenied
            obj = None

        else:
            obj = self.get_object(request, unquote(object_id), to_field)

            if request.method == "POST":
                if not self.has_change_permission(request, obj):
                    raise PermissionDenied
            else:
                if not self.has_view_or_change_permission(request, obj):
                    raise PermissionDenied

            if obj is None:
                return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        fieldsets = self.get_fieldsets(request, obj)
        ModelForm = self.get_form(
            request, obj, change=not add, fields=flatten_fieldsets(fieldsets)
        )

        if request.method == "POST":
            form = ModelForm(request.POST, request.FILES, instance=obj)
            formsets, inline_instances = self._create_formsets(
                request,
                form.instance,
                change=not add,
            )
            # 加锁
            lock_id = f'meetroom_{form.instance.room_id}'
            lock = CacheLock(lock_id, expires=1 * 60 * 60, wait_timeout=10)  # 最长1分钟释放 等锁时间最长10秒
            lock.acquire_lock()

            form_validated = form.is_valid()

            if form_validated:
                new_object = self.save_form(request, form, change=not add)
            else:
                new_object = form.instance
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, not add)
                self.save_related(request, form, formsets, not add)
                if lock:
                    lock.release_lock()
                change_message = self.construct_change_message(
                    request, form, formsets, add
                )
                if add:
                    self.log_addition(request, new_object, change_message)
                    return self.response_add(request, new_object)
                else:
                    self.log_change(request, new_object, change_message)
                    return self.response_change(request, new_object)
            else:
                form_validated = False

            lock.release_lock()  # 解锁 仅改了加锁解锁 其它未变化。
        else:
            if add:
                initial = self.get_changeform_initial_data(request)
                form = ModelForm(initial=initial)
                formsets, inline_instances = self._create_formsets(
                    request, form.instance, change=False
                )
            else:
                form = ModelForm(instance=obj)
                formsets, inline_instances = self._create_formsets(
                    request, obj, change=True
                )


        if not add and not self.has_change_permission(request, obj):
            readonly_fields = flatten_fieldsets(fieldsets)
        else:
            readonly_fields = self.get_readonly_fields(request, obj)
        adminForm = helpers.AdminForm(
            form,
            list(fieldsets),
            # Clear prepopulated fields on a view-only form to avoid a crash.
            self.get_prepopulated_fields(request, obj)
            if add or self.has_change_permission(request, obj)
            else {},
            readonly_fields,
            model_admin=self,
        )
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(
            request, formsets, inline_instances, obj
        )
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        if add:
            title = _("Add %s")
        elif self.has_change_permission(request, obj):
            title = _("Change %s")
        else:
            title = _("View %s")
        context = {
            **self.admin_site.each_context(request),
            "title": title % opts.verbose_name,
            "subtitle": str(obj) if obj else None,
            "adminform": adminForm,
            "object_id": object_id,
            "original": obj,
            "is_popup": IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET,
            "to_field": to_field,
            "media": media,
            "inline_admin_formsets": inline_formsets,
            "errors": helpers.AdminErrorList(form, formsets),
            "preserved_filters": self.get_preserved_filters(request),
        }

        # Hide the "Save" and "Save and continue" buttons if "Save as New" was
        # previously chosen to prevent the interface from getting confusing.
        if (
            request.method == "POST"
            and not form_validated
            and "_saveasnew" in request.POST
        ):
            context["show_save"] = False
            context["show_save_and_continue"] = False
            # Use the change template instead of the add template.
            add = False

        context.update(extra_context or {})

        return self.render_change_form(
            request, context, add=add, change=not add, obj=obj, form_url=form_url
        )

    """
        不得不重写这一大段代码 这就是大家不爱用django crontrib admin 以及 form去开发的原因吧
    """

    # def save_model(self, request, obj, form, change):
    #     """
    #     Given a model instance save it to the database.
    #     """
    #     obj.save()
    #     if hasattr(self, 'lock'):
    #         self.lock.release_lock()
    """
        此处编码方式极其怪异，之所以大家开发往往不按django crontrib form去开发 就是这种问题，
        规定的结构太细太死，加一个锁 是改在is_valid 上 还是改在save_form还是save_model上？都不对
        一般开发请参考views代码。
        但因为django.crontrib.admin的开发方式酷似低代码研发方式，以及为快速提供前端界面，故特意以它进行了一次演示开发。
    """




admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingRoom, MeetRoomAdmin)
