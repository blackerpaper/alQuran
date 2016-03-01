# -*- coding: utf-8 -*-
import codecs
import operator


class AlQuran:
    def __init__(self):
        self.alQuran = self.parsingAlQuran()

    def parsingAlQuran(self):
        dokumen = codecs.open('quran.txt', encoding='utf-8')
        alQuran = [[[]]]

        for baris in dokumen:
            parsing = baris.strip().split('|')
            noSurat = int(parsing[0])
            noAyat = int(parsing[1])
            noKata = int(parsing[2])
            kata = parsing[3]
            kataHarokat = parsing[4]
            terjemah = parsing[5]

            while len(alQuran) < noSurat:                           alQuran.append([])
            while len(alQuran[noSurat - 1]) < noAyat:               alQuran[noSurat - 1].append([])
            while len(alQuran[noSurat - 1][noAyat - 1]) < noKata:   alQuran[noSurat - 1][noAyat - 1].append([])

            alQuran[noSurat - 1][noAyat - 1][noKata - 1] = [kata, kataHarokat, terjemah]

        return alQuran

    # Mengambil kata pada alQuran
    # Misal: ambil(1, 2, 3) -> mengambil kata dari surat alfatihah ayat 2 kata ke-3
    def ambil(self, noSurat, noAyat, noKata):
        return self.alQuran[noSurat - 1][noAyat - 1][noKata - 1][0]

    # Menghitung kemunculan kata didalam alQuran
    # Misal: hitung(u'الله') -> menghitung kemunculan kata الله
    def hitung(self, kata, dariNoSurat=0, keNoSurat=0):
        hitung = 0

        if not dariNoSurat: dariNoSurat = 1
        if not keNoSurat:   keNoSurat = len(self.alQuran) + 1

        for noSurat in range(dariNoSurat, keNoSurat):
            for noAyat in range(1, self.jumlahAyat(noSurat) + 1):
                for noKata in range(1, self.jumlahKata(noSurat, noAyat) + 1):
                    hitung = hitung + self.ambil(noSurat, noAyat, noKata).count(kata)

        return hitung

    # Membuat histogram kemunculan kata yg ada didalam alQuran
    # Misal: histogram(1, 2) -> histogram dari surat alfatihah
    def histogram(self, dariNoSurat=0, keNoSurat=0):
        histogram = {}

        if not dariNoSurat: dariNoSurat = 1
        if not keNoSurat:   keNoSurat = len(self.alQuran) + 1

        for noSurat in range(dariNoSurat, keNoSurat):
            for noAyat in range(1, self.jumlahAyat(noSurat) + 1):
                for noKata in range(1, self.jumlahKata(noSurat, noAyat) + 1):
                    kata = self.ambil(noSurat, noAyat, noKata)
                    if not kata in histogram:
                        histogram[kata] = 1
                    else:
                        histogram[kata] = histogram[kata] + 1

        return histogram

    def tengahSurat(self, noSurat):
        jumlahTengahKata = self.jumlahKata(noSurat) / 2

        jumlahKata = 0
        for noAyat in range(1, self.jumlahAyat(noSurat) + 1):
            jumlahKataDalamAyat = self.jumlahKata(noSurat, noAyat)
            jumlahKata = jumlahKata + jumlahKataDalamAyat
            if jumlahKata >= jumlahTengahKata:
                tengahKata = jumlahKataDalamAyat - (jumlahKata - jumlahTengahKata)
                return self.ambil(noSurat, noAyat, tengahKata)

    def terjemah(self, cari):
        for surat in self.alQuran:
            for ayat in surat:
                for kata in ayat:
                    if kata[0] == cari:
                        return kata[2]

    def jumlahSurat(self):
        return len(self.alQuran)

    def jumlahAyat(self, noSurat):
        return len(self.alQuran[noSurat - 1])

    def jumlahKata(self, noSurat, noAyat=0):
        jumlahKata = 0
        if not noAyat:
            for noAyat in range(1, self.jumlahAyat(noSurat) + 1):
                jumlahKata = jumlahKata + self.jumlahKata(noSurat, noAyat)
        else:
            jumlahKata = len(self.alQuran[noSurat - 1][noAyat - 1])

        return jumlahKata

    def jumlahHuruf(self, noSurat, noAyat, noKata):
        return len(self.alQuran[noSurat - 1][noAyat - 1][noKata - 1][0])

    def cariTerjemah(self, kata):
        ketemu = []
        for noSurat in range(1, self.jumlahSurat() + 1):
            for noAyat in range(1, self.jumlahAyat(noSurat) + 1):
                for noKata in range(1, self.jumlahKata(noSurat, noAyat) + 1):
                    if self.alQuran[noSurat - 1][noAyat - 1][noKata - 1][2].count(kata):
                        ketemu.append((noSurat, noAyat, noKata))

        return ketemu

    def cariAkarKata(self, akarKata):
        kelompok = []
        for noSurat in range(1, self.jumlahSurat() + 1):
            for noAyat in range(1, self.jumlahAyat(noSurat) + 1):
                for noKata in range(1, self.jumlahKata(noSurat, noAyat) + 1):
                    indeks = 0
                    kata = self.ambil(noSurat, noAyat, noKata)
                    for noHuruf in range(1, self.jumlahHuruf(noSurat, noAyat, noKata) + 1):
                        if kata[noHuruf - 1].count(akarKata[indeks]):
                            if indeks < len(akarKata):
                                indeks = indeks + 1
                                if indeks >= len(akarKata): break
                            else:
                                break
                    if indeks == len(akarKata):
                        kelompok.append((noSurat, noAyat, noKata))
        return kelompok


alQuran = AlQuran()

histogram = {}
kelompok = alQuran.cariAkarKata((u'ق', u'ل', u'ب'))
for i in kelompok:
    surat = i[0]
    if not surat in histogram:
        histogram[surat] = 1
    else:
        histogram[surat] = histogram[surat] + 1

histogramUrut = sorted(histogram.items(), key=operator.itemgetter(1))
for el in histogramUrut:
    kemunculan = float(el[1]) / float(alQuran.jumlahAyat(el[0])) * 100
    print u'%s:\t\t%d\t\t%.2f' % (el[0], el[1], kemunculan)



# ketemu = alQuran.cariTerjemah(u"hati")
# for i in ketemu:
#     print u'%d:%d - %s' % (i[0], i[1], alQuran.ambil(i[0], i[1], i[2]))

# histogram = alQuran.histogram(36, 37)
# histogramUrut = sorted(histogram.items(), key=operator.itemgetter(1))
# for el in histogramUrut:
#     print u'%s: %d' % (el[0], el[1])

# print(alQuran.tengahSurat(1))

# print(alQuran.hitung(u'الله'))

# for i in range(1, 115):
#     sum = 0
#     histogram = alQuran.histogram(i, i+1)
#     histogramUrut = sorted(histogram.items(), key=operator.itemgetter(1))
#     for el in histogramUrut:
#         sum = sum + el[1]
#
#     hitung = alQuran.hitung(u'الله', i, i+1)
#     print u'%d:\t\t%d\t\t%d\t\t%.2f%%' % (i, sum, hitung, 100 * float(hitung) / float(sum))
