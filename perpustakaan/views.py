from django.shortcuts import render, redirect, get_object_or_404
from .models import Buku, Peminjaman
from django.db.models import Sum

# ================= DASHBOARD =================
def dashboard(request):
    total_buku = Buku.objects.aggregate(Sum('stok'))['stok__sum'] or 0
    total_judul = Buku.objects.count()
    sedang_dipinjam = Peminjaman.objects.count()  # Membaca total dari tabel peminjam SQL
    sudah_kembali = 0  # Karena di SQL manualmu tidak ada kolom status kembali
    
    daftar_buku = Buku.objects.all()
    
    context = {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_kembali': sudah_kembali,
        'daftar_buku': daftar_buku,
    }
    return render(request, 'perpustakaan/dashboard.html', context)

# ================= KELOLA BUKU =================
def daftar_buku(request):
    buku = Buku.objects.all()
    return render(request, 'perpustakaan/daftar_buku.html', {'daftar_buku': buku})

def tambah_buku(request):
    if request.method == 'POST':
        Buku.objects.create(
            judul=request.POST['judul'],
            pengarang=request.POST['pengarang'],
            stok=request.POST['stok'],
            tahun_terbit=request.POST.get('tahun_terbit', None)
        )
        return redirect('daftar_buku')
    return render(request, 'perpustakaan/form_buku.html', {'aksi': 'Tambah'})

def detail_buku(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    return render(request, 'perpustakaan/detail_buku.html', {'buku': buku})

def edit_buku(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    if request.method == 'POST':
        buku.judul = request.POST['judul']
        buku.pengarang = request.POST['pengarang']
        buku.stok = request.POST['stok']
        buku.tahun_terbit = request.POST.get('tahun_terbit', None)
        buku.save()
        return redirect('daftar_buku')
    return render(request, 'perpustakaan/form_buku.html', {'buku': buku, 'aksi': 'Edit'})

def hapus_buku(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    if request.method == 'POST':
        buku.delete()
        return redirect('daftar_buku')
    return render(request, 'perpustakaan/hapus_konfirmasi.html', {'item': buku, 'tipe': 'Buku', 'cancel_url': 'daftar_buku'})

# ================= TRANSAKSI PEMINJAMAN =================
def daftar_peminjaman(request):
    peminjaman = Peminjaman.objects.all()
    return render(request, 'perpustakaan/daftar_peminjaman.html', {'daftar_peminjaman': peminjaman})

def pinjam_buku(request):
    if request.method == 'POST':
        nama_peminjam = request.POST.get('peminjam')
        buku_id = request.POST.get('buku')
        tanggal_pinjam = request.POST.get('tanggal_pinjam')
        jatuh_tempo = request.POST.get('jatuh_tempo')
        keperluan = request.POST.get('keperluan')
        catatan = request.POST.get('catatan') 

        # 1. Ambil object buku yang dipilih
        buku = get_object_or_404(Buku, pk=buku_id)

        # Cek apakah stok buku masih ada sebelum membolehkan pinjam
        if buku.stok > 0:
            # 2. Buat data transaksi peminjaman baru
            Peminjaman.objects.create(
                nama_peminjam=nama_peminjam,
                id_buku=buku, 
                status_kembali='Dipinjam', 
            )

            # 3. Potong stok buku asal sebanyak 1
            buku.stok -= 1
            buku.save()

        return redirect('daftar_peminjaman')

    # Jika akses biasa (GET), ambil semua buku untuk dropdown form
    daftar_buku = Buku.objects.filter(stok__gt=0) 
    return render(request, 'perpustakaan/form_peminjaman.html', {'daftar_buku': daftar_buku})

def kembalikan_buku(request, pk):
    peminjaman = get_object_or_404(Peminjaman, pk=pk)
    
    if peminjaman.status_kembali == 'Dipinjam':
        peminjaman.status_kembali = 'Dikembalikan'
        peminjaman.save()
        
        buku = peminjaman.id_buku
        buku.stok += 1
        buku.save()
        
    return redirect('daftar_peminjaman')

# ================= FITUR USER / ANGGOTA SISWA =================
# Menggunakan data simulasi (Dummy) sepenuhnya agar aman dari ImportError
def daftar_user(request):
    users = [
        {'pk': 1, 'id': 1, 'nama': 'Roni', 'kelas': 'XI IPA 1', 'nis': '2026001', 'status': 'Aktif'},
        {'pk': 2, 'id': 2, 'nama': 'Sinta', 'kelas': 'XI IPS 2', 'nis': '2026002', 'status': 'Aktif'},
        {'pk': 3, 'id': 3, 'nama': 'Dewi Anggraini', 'kelas': 'X IPA 3', 'nis': '2026003', 'status': 'Aktif'},
        {'pk': 4, 'id': 4, 'nama': 'Bima Pratama', 'kelas': 'XII IPS 1', 'nis': '2026004', 'status': 'Aktif'},
    ]
    return render(request, 'perpustakaan/daftar_user.html', {'daftar_user': users})

def tambah_user(request):
    if request.method == 'POST':
        return redirect('daftar_user')
    return render(request, 'perpustakaan/form_user.html')

def detail_user(request, pk):
    user_data = {'id': pk, 'nama': 'Roni', 'kelas': 'XI IPA 1', 'nis': '2026001'} 
    return render(request, 'perpustakaan/detail_user.html', {'user_member': user_data})

def edit_user(request, pk):
    if request.method == 'POST':
        return redirect('daftar_user')
    user_data = {'id': pk, 'nama': 'Roni', 'kelas': 'XI IPA 1', 'nis': '2026001'} 
    return render(request, 'perpustakaan/form_user.html', {'user_member': user_data})

def hapus_user(request, pk):
    if request.method == 'POST':
        return redirect('daftar_user')
    user_data = {'nama': 'Dewi Anggraini'} 
    return render(request, 'perpustakaan/hapus_konfirmasi.html', {'item': user_data, 'tipe': 'User', 'cancel_url': 'daftar_user'})