from django.db import models

class Buku(models.Model):
    # Django butuh primary key, karena di SQL kamu pakai SERIAL, kita set manual di sini
    id = models.AutoField(primary_key=True)
    judul = models.CharField(max_length=150)
    pengarang = models.CharField(max_length=100) # Sudah disesuaikan dengan RENAME COLUMN di psql kamu
    stok = models.IntegerField(default=0)
    tahun_terbit = models.IntegerField(null=True, blank=True) # Sesuai ADD COLUMN kamu

    class Meta:
        db_table = 'buku' # MEMAKSA Django membaca tabel 'buku' di SQL-mu

    def __str__(self):
        return self.judul


class Peminjaman(models.Model):
    id_peminjam = models.AutoField(primary_key=True)
    nama_peminjam = models.CharField(max_length=100)
    # Relasi foreign key ke tabel buku murni SQL-mu
    id_buku = models.ForeignKey(Buku, on_delete=models.CASCADE, db_column='id_buku')

    class Meta:
        db_table = 'peminjam' # MEMAKSA Django membaca tabel 'peminjam' di SQL-mu

    def __str__(self):
        return f"{self.nama_peminjam} pinjam {self.id_buku.judul}"