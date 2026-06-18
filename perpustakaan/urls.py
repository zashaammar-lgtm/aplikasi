from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('buku/', views.daftar_buku, name='daftar_buku'),
    path('buku/tambah/', views.tambah_buku, name='tambah_buku'),
    path('buku/<int:pk>/', views.detail_buku, name='detail_buku'),
    path('buku/<int:pk>/edit/', views.edit_buku, name='edit_buku'),
    path('buku/<int:pk>/hapus/', views.hapus_buku, name='hapus_buku'),
    
    path('user/', views.daftar_user, name='daftar_user'),
    path('user/tambah/', views.tambah_user, name='tambah_user'),
    path('user/<int:pk>/', views.detail_user, name='detail_user'),
    path('user/<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('user/<int:pk>/hapus/', views.hapus_user, name='hapus_user'),
    
    path('peminjaman/', views.daftar_peminjaman, name='daftar_peminjaman'),
    path('peminjaman/baru/', views.pinjam_buku, name='pinjam_buku'),
    path('peminjaman/<int:pk>/kembali/', views.kembalikan_buku, name='kembalikan_buku'),
]