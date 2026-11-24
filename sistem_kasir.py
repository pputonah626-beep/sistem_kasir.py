class Produk:
    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self.stok = stok

    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, nilai):
        if nilai < 0:
            raise ValueError("Harga tidak boleh negatif")
        self.__harga = nilai

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, nilai):
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif")
        self.__stok = nilai

    @classmethod
    def dari_teks(cls, data):
        nama, harga, stok = data.split(",")
        return cls(nama.strip(), int(harga), int(stok))


class Transaksi:
    def __init__(self, daftar, total, diskon, bayar, kembali):
        self.daftar = daftar
        self.total = total
        self.diskon = diskon
        self.bayar = bayar
        self.kembali = kembali


class Kasir:
    BATAS_DISKON = 100000
    PERSEN_DISKON = 10

    def __init__(self):
        self.__produk = {}
        self.__keranjang = {}
        self.__riwayat = []

    @staticmethod
    def rupiah(nilai):
        return f"Rp{nilai:,.0f}".replace(",", ".")

    @classmethod
    def hitung_diskon(cls, total):
        if total >= cls.BATAS_DISKON:
            return total * cls.PERSEN_DISKON // 100
        return 0

    def tambah_produk(self, nama, harga, stok):
        self.__produk[nama] = Produk(nama, harga, stok)
        print("Produk berhasil ditambahkan.")

    def tampil_produk(self):
        print("\n--- DAFTAR PRODUK ---")
        if not self.__produk:
            print("Belum ada produk.")
        for p in self.__produk.values():
            print(f"{p.nama} | {self.rupiah(p.harga)} | Stok: {p.stok}")

    def ubah_produk(self, nama, harga, stok):
        if nama not in self.__produk:
            print("Produk tidak ditemukan.")
            return
        self.__produk[nama].harga = harga
        self.__produk[nama].stok = stok
        print("Produk berhasil diperbarui.")

    def tambah_keranjang(self, nama, jumlah):
        if nama not in self.__produk:
            print("Produk tidak ditemukan.")
            return

        p = self.__produk[nama]
        sudah = self.__keranjang.get(nama, 0)

        if jumlah <= 0 or sudah + jumlah > p.stok:
            print("Jumlah tidak valid atau stok tidak cukup.")
            return

        self.__keranjang[nama] = sudah + jumlah
        print("Barang masuk keranjang.")

    def lihat_keranjang(self):
        print("\n--- KERANJANG ---")
        if not self.__keranjang:
            print("Keranjang kosong.")

        for nama, jumlah in self.__keranjang.items():
            p = self.__produk[nama]
            subtotal = p.harga * jumlah
            print(f"{nama} x{jumlah} = {self.rupiah(subtotal)}")

    def hapus_keranjang(self, nama):
        if nama in self.__keranjang:
            del self.__keranjang[nama]
            print("Barang berhasil dihapus.")
        else:
            print("Barang tidak ada di keranjang.")

    def checkout(self):
        if not self.__keranjang:
            print("Keranjang masih kosong.")
            return

        daftar = []
        total = 0

        for nama, jumlah in self.__keranjang.items():
            p = self.__produk[nama]
            subtotal = p.harga * jumlah
            daftar.append((nama, jumlah, p.harga, subtotal))
            total += subtotal

        diskon = self.hitung_diskon(total)
        tagihan = total - diskon

        print("\nTotal:", self.rupiah(total))
        print("Diskon:", self.rupiah(diskon))
        print("Total bayar:", self.rupiah(tagihan))

        try:
            bayar = int(input("Uang pembayaran: Rp"))
        except ValueError:
            print("Masukkan angka yang benar.")
            return

        if bayar < tagihan:
            print("Uang pembayaran kurang.")
            return

        kembali = bayar - tagihan

        for nama, jumlah, harga, subtotal in daftar:
            self.__produk[nama].stok -= jumlah

        transaksi = Transaksi(daftar, total, diskon, bayar, kembali)
        self.__riwayat.append(transaksi)

        print("\n====== STRUK TOKO MAJU JAYA ======")
        for nama, jumlah, harga, subtotal in daftar:
            print(f"{nama} ({jumlah} x {self.rupiah(harga)}) = {self.rupiah(subtotal)}")

        print("---------------------------------")
        print("Subtotal :", self.rupiah(total))
        print("Diskon   :", self.rupiah(diskon))
        print("Total    :", self.rupiah(tagihan))
        print("Bayar    :", self.rupiah(bayar))
        print("Kembali  :", self.rupiah(kembali))
        print("Terima kasih telah berbelanja!")

        self.__keranjang.clear()

    def riwayat_transaksi(self):
        print("\n--- RIWAYAT TRANSAKSI ---")
        if not self.__riwayat:
            print("Belum ada transaksi.")

        for i, t in enumerate(self.__riwayat, 1):
            print(f"{i}. Total: {self.rupiah(t.total - t.diskon)}")

    def laporan_penjualan(self):
        print("\n--- LAPORAN PENJUALAN ---")
        if not self.__riwayat:
            print("Belum ada penjualan.")
            return

        total = sum(t.total - t.diskon for t in self.__riwayat)
        jumlah = sum(len(t.daftar) for t in self.__riwayat)

        print("Jumlah transaksi:", len(self.__riwayat))
        print("Jenis barang terjual:", jumlah)
        print("Pendapatan:", self.rupiah(total))


def main():
    kasir = Kasir()

    while True:
        print("""
===== SISTEM KASIR TOKO MAJU JAYA =====
1. Tampilkan produk
2. Tambah produk
3. Ubah produk
4. Tambah ke keranjang
5. Lihat keranjang
6. Hapus dari keranjang
7. Checkout / Bayar
8. Riwayat transaksi
9. Laporan penjualan
0. Keluar
""")

        pilih = input("Pilih menu: ")

        try:
            if pilih == "1":
                kasir.tampil_produk()

            elif pilih == "2":
                nama = input("Nama produk: ")
                harga = int(input("Harga: "))
                stok = int(input("Stok: "))
                kasir.tambah_produk(nama, harga, stok)

            elif pilih == "3":
                nama = input("Nama produk: ")
                harga = int(input("Harga baru: "))
                stok = int(input("Stok baru: "))
                kasir.ubah_produk(nama, harga, stok)

            elif pilih == "4":
                nama = input("Nama produk: ")
                jumlah = int(input("Jumlah: "))
                kasir.tambah_keranjang(nama, jumlah)

            elif pilih == "5":
                kasir.lihat_keranjang()

            elif pilih == "6":
                nama = input("Nama produk yang dihapus: ")
                kasir.hapus_keranjang(nama)

            elif pilih == "7":
                kasir.checkout()

            elif pilih == "8":
                kasir.riwayat_transaksi()

            elif pilih == "9":
                kasir.laporan_penjualan()

            elif pilih == "0":
                print("Program selesai.")
                break

            else:
                print("Menu tidak tersedia.")

        except ValueError:
            print("Input harus berupa angka yang valid.")


if __name__ == "__main__":
    main()