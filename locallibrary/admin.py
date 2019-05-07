from collections import defaultdict, OrderedDict

from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.urls import path

from catalog.temp_db.info import get_not_accepted_data, check_for_changes, smart_counter, smart_cleaner, TRACKED_MODELS


def _form_handler(action, selected):
    mapping = defaultdict(list)
    for key in selected:
        model, pk = key.split('-')
        mapping[model].append(pk)

    for m in TRACKED_MODELS:
        if m.name in mapping:
            selected_objects = m.model.objects.using('temp').filter(pk__in=mapping[m.name])
            if action == 'Store':
                # can we make a bulk creation instead of this?
                for obj in selected_objects:
                    auto_saved_objects = []
                    try:
                        # storig temp object in default db
                        m.saver(obj, auto_saved_objects)
                    except Exception:
                        pass
                    finally:
                        # remove this obj
                        obj.delete()
                        # clear auto saved objects without another links
                        smart_cleaner(auto_saved_objects)
            elif action == 'Delete':
                selected_objects.delete()


class CustomAdminSite(AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('changes/', self.admin_view(self.changes), name="see_changes")
        ]
        return my_urls + urls

    def changes(self, request):
        if request.POST.get('_action_', None) in ('Store', 'Delete'):
            selected = list(k for k in request.POST.keys() if k not in ('csrfmiddlewaretoken', '_action_'))
            _form_handler(request.POST['_action_'], selected)

        context = self.each_context(request)
        context['changes'] = get_not_accepted_data() if context['changes_exists'] else []
        context['add_watch_link'] = False

        return render(request, 'admin/see_temp.html', context)

    def each_context(self, request):
        context = super().each_context(request)
        context['changes_exists'] = check_for_changes()
        # this one needed in all cases:
        context['changes_counts'] = OrderedDict((m.name, smart_counter(m.model)) for m in TRACKED_MODELS)
        context['add_watch_link'] = True

        return context
