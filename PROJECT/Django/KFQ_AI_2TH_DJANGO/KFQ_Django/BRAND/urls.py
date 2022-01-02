from django.urls import path
from BRAND import views
from .VIEW.theme import Theme
from .VIEW.account import Account

app_name='BRAND'

urlpatterns = [
    path('test/', views.index),
    path('index/', views.Brand.index, name='index'),
    path('about/', views.Brand.aboutus, name='about'),
    path('features/', views.Brand.features, name='features'),
    path('hosting/', views.Brand.hosting, name='hosting'),
    path('domain/', views.Brand.domain, name='domain'),
    path('pricing/', views.Brand.pricing, name='pricing'),
    path('contact/', views.Brand.contact, name='contact'),
#***********************************************************************#
    # Original Theme
    path('theme/index/', Theme.theme_index, name='1_index.html'),
    path('theme/about/', Theme.theme_aboutus, name='2_about.html'),
    path('theme/features/', Theme.theme_features, name='3_features.html'),
    path('theme/hosting/', Theme.theme_hosting, name='4_hosting.html'),
    path('theme/domain/', Theme.theme_domain, name='5_domain.html'),
    path('theme/pricing/', Theme.theme_pricing, name='6_pricing.html'),
    path('theme/contact/', Theme.theme_contact, name='7_contact.html'),
#***********************************************************************#
    path('signup/', Account.signup, name="signup"),
    path('signin/', Account.signin, name="signin"),
    path('signout/', Account.signout, name="signout"),
    path('find_password/', Account.find_password, name='find_password'),
#***********************************************************************#
]