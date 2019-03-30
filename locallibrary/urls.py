from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('editor/', include('editor.urls', namespace='editor')),
    # блэт! никогда не ставь permanent=True - после этого надо заебываться с чисткой браузерного кеша,
    # если вдруг решили поменять путь (собсно как сейчас и произошло). Потом как будет всё говотово - выставим как надо.
    # path('catalog/', RedirectView.as_view(url='/catalog/', permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
