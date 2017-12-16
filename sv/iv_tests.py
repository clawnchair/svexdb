import unittest
from sv import iv


class PerfectIVChecker(unittest.TestCase):
    def test_keybv(self):
        self.assertTrue(iv.is_perfect("~ - 3 - Espurr (♀) - Timid - Keen Eye - 31.26.31.31.31.31 - Dragon - [1977]"))

    def test_keysav1(self):
        self.assertFalse(iv.is_perfect("| B18 | 1,3 | Honedge (M) | Adamant | No Guard | 31.31.31.31.01.31 | 0184 |"))
        self.assertTrue(iv.is_perfect("B1 - 3,4 - Aipom エイパム (M) - Jolly - Run Away - 31.31.31.26.31.31 [0766] - Electric"))
        self.assertFalse(iv.is_perfect("B1 - 3,4 - Aipom エイパム (M) - Jolly - Run Away - 31.31.28.26.31.31 [0766] - Electric"))
        self.assertFalse(iv.is_perfect("| B4 | 3,3 | Carbink | Bold | Sturdy | 31.31.31.19.31.31 | 3827 |"))
        self.assertTrue(iv.is_perfect("| B4 | 3,3 | Carbink | Bold | Sturdy | 31.01.31.31.31.31 | 3827 |"))
        self.assertTrue(iv.is_perfect("| 2,1 | Corsola (F) | Bold | Hustle       | 31/08/31/31/31/31 | 1506 | Dragon |"))
        self.assertTrue(iv.is_perfect("| B2 | 1,5 | Phantump (F) | Impish | Frisk | 31.31.30.31.31.31 | 3809 |"))
        self.assertTrue(iv.is_perfect("| B2 | 1,5 | Phantump (F) | Impish | Frisk | 30.30.30.30.30.30 | 3809 |"))
        self.assertFalse(iv.is_perfect("| B2 | 1,5 | Phantump (F) | Impish | Frisk | 30.29.30.31.31.31 | 3809 |"))

    def test_keysav2(self):
        self.assertFalse(iv.is_perfect("B01 - 1,5 - Wailmer (♂) - Modest - Water Veil - 31.31.31.31.31.18 - Ice - [2431]"))
        self.assertTrue(iv.is_perfect("B04 - 2,6 - Carbink (-) - Bold - Sturdy - 31.28.31.31.31.31 - Dragon - [3439]"))
        self.assertTrue(iv.is_perfect("B17 - 2,6 - Salamèche (♂) - Bold - Chlorophyll - 31.0.31.30.31.30 - Fire"))


    def test_fork(self):
        self.assertTrue(iv.is_perfect("| 1,6 | Heracross (F) | Jolly | Swarm | 31/31/31/17/31/31 | [1633] | Love Ball | Dark |"))

    def test_eng(self):
        self.assertTrue(iv.is_perfect("B14 - 4,3 - Roggenrola (♂) - Brave - Sand Force - 31.31.31.31.31.1 - Dark - [0009]")) #brave
        self.assertTrue(iv.is_perfect("B14 - 3,6 - Pancham (♀) - Adamant - Iron Fist - 31.31.31.19.31.31 - Dark - [0814]")) #adamant
        self.assertTrue(iv.is_perfect("B14 - 3,1 - Klefki (♀) - Bold - Magician - 31.4.31.31.31.31 - Dragon - [3914]")) #bold
        self.assertTrue(iv.is_perfect("B24 - 4,2 - Porygon (♀) - Relaxed - Analytic - 31.31.31.31.31.11 - Dark - ")) #relaxed
        self.assertTrue(iv.is_perfect("B08 - 1,4 - Furfrou (♀) - Impish - Fur Coat - 31.31.31.11.31.31 - Dark - [3345]")) #impish
        self.assertTrue(iv.is_perfect("B14 - 1,1 - Noibat (♂) - Timid - Frisk - 31.25.31.31.31.31 - Dark - [2393]")) #timid
        self.assertTrue(iv.is_perfect("B10 - 3,6 - Tirtouga (♀) - Jolly - Swift Swim - 31.31.31.20.31.31 - Electric - ")) #jolly
        self.assertTrue(iv.is_perfect("B14 - 5,1 - Bulbasaur (♂) - Modest - Chlorophyll - 31.11.31.31.31.31 - Dark - [3455]")) #modest
        self.assertTrue(iv.is_perfect("B14 - 5,4 - Amaura (♂) - Quiet - Refrigerate - 31.31.31.31.31.0 - Psychic - [0132]")) #quiet
        self.assertTrue(iv.is_perfect("B14 - 4,5 - Goomy (♀) - Calm - Gooey - 31.1.31.31.31.31 - Dark - [1478]")) #calm
        self.assertTrue(iv.is_perfect("B27 - 4,1 - Binacle (♀) - Sassy - Pickpocket - 31.31.31.31.31.24 - Ice - ")) #sassy
        self.assertTrue(iv.is_perfect("B27 - 3,6 - Ditto (-) - Careful - Limber - 31.31.31.20.31.31 - Dark - ")) #careful

    def test_jpn(self):
        self.assertTrue(iv.is_perfect("B14 - 4,3 - ダンゴロ (♂) - ゆうかん - すなのちから - 31.31.31.31.31.1 - あく - [0009]")) #brave
        self.assertTrue(iv.is_perfect("B14 - 3,6 - ヤンチャム (♀) - いじっぱり - てつのこぶし - 31.31.31.19.31.31 - あく - [0814]")) #adamant
        self.assertTrue(iv.is_perfect("B14 - 3,1 - クレッフィ (♀) - ずぶとい - マジシャン - 31.4.31.31.31.31 - ドラゴン - [3914]")) #bold
        self.assertTrue(iv.is_perfect("B24 - 4,2 - ポリゴン (♀) - のんき - アナライズ - 31.31.31.31.31.1 - あく - ")) #relaxed
        self.assertTrue(iv.is_perfect("B08 - 1,4 - トリミアン (♀) - わんぱく - ファーコート - 31.31.31.11.31.31 - あく - [3345]")) #impish
        self.assertTrue(iv.is_perfect("B14 - 1,1 - オンバット (♂) - おくびょう - おみとおし - 31.25.31.31.31.31 - あく - [2393]")) #timid
        self.assertTrue(iv.is_perfect("B10 - 3,6 - プロトーガ (♀) - ようき - すいすい - 31.31.31.20.31.31 - でんき - ")) #jolly
        self.assertTrue(iv.is_perfect("B14 - 5,1 - フシギダネ (♂) - ひかえめ - ようりょくそ - 31.11.31.31.31.31 - あく - [3455]")) #modest
        self.assertTrue(iv.is_perfect("B14 - 5,4 - アマルス (♂) - れいせい - フリーズスキン - 31.31.31.31.31.0 - エスパー - [0132]")) #quiet
        self.assertTrue(iv.is_perfect("B14 - 4,5 - ヌメラ (♀) - おだやか - ぬめぬめ - 31.1.31.31.31.31 - あく - [1478]")) #calm
        self.assertTrue(iv.is_perfect("B27 - 4,1 - カメテテ (♀) - なまいき - わるいてぐせ - 31.31.31.31.31.24 - こおり - ")) #sassy
        self.assertTrue(iv.is_perfect("B27 - 3,6 - メタモン (-) - しんちょう - じゅうなん - 31.31.31.20.31.31 - あく - ")) #careful

    def test_french(self):
        self.assertTrue(iv.is_perfect("B14 - 4,3 - Nodulithe (♂) - Brave - Force Sable - 31.31.31.31.31.1 - Ténèbres - [0009]")) #brave
        self.assertTrue(iv.is_perfect("B14 - 3,6 - Pandespiègle (♀) - Rigide - Poing de Fer - 31.31.31.19.31.31 - Ténèbres - [0814]")) #adamant
        self.assertTrue(iv.is_perfect("B14 - 3,1 - Trousselin (♀) - Assuré - Magicien - 31.4.31.31.31.31 - Dragon - [3914]")) #bold
        self.assertTrue(iv.is_perfect("B24 - 4,2 - Porygon (♀) - Relax - Analyste - 31.31.31.31.31.1 - Ténèbres - ")) #relaxed
        self.assertTrue(iv.is_perfect("B08 - 1,4 - Couafarel (♀) - Malin - Toison Épaisse - 31.31.31.11.31.31 - Ténèbres - [3345]")) #impish
        self.assertTrue(iv.is_perfect("B14 - 1,1 - Sonistrelle (♂) - Timide - Fouille - 31.25.31.31.31.31 - Ténèbres - [2393]")) #timid
        self.assertTrue(iv.is_perfect("B10 - 3,6 - Carapagos (♀) - Jovial - Glissade - 31.31.31.20.31.31 - Électrik - ")) #jolly
        self.assertTrue(iv.is_perfect("B14 - 5,1 - Bulbizarre (♂) - Modeste - Chlorophylle - 31.11.31.31.31.31 - Ténèbres - [3455]")) #modest
        self.assertTrue(iv.is_perfect("B14 - 5,4 - Amagara (♂) - Discret - Peau Gelée - 31.31.31.31.31.0 - Psy - [0132]")) #quiet
        self.assertTrue(iv.is_perfect("B14 - 4,5 - Mucuscule (♀) - Calme - Poisseux - 31.1.31.31.31.31 - Ténèbres - [1478]")) #calm
        self.assertTrue(iv.is_perfect("B27 - 4,1 - Opermine (♀) - Malpoli - Pickpocket - 31.31.31.31.31.24 - Glace - ")) #sassy
        self.assertTrue(iv.is_perfect("B27 - 3,6 - Métamorph (-) - Prudent - Échauffement - 31.31.31.20.31.31 - Ténèbres - ")) #careful

    def test_ita(self):
        self.assertTrue(iv.is_perfect("B14 - 4,3 - Roggenrola (♂) - Audace - Silicoforza - 31.31.31.31.31.1 - Buio - [0009]")) #brave
        self.assertTrue(iv.is_perfect("B14 - 3,6 - Pancham (♀) - Decisa - Ferropugno - 31.31.31.19.31.31 - Buio - [0814]")) #adamant
        self.assertTrue(iv.is_perfect("B14 - 3,1 - Klefki (♀) - Sicura - Prestigiatore - 31.4.31.31.31.31 - Drago - [3914]")) #bold
        self.assertTrue(iv.is_perfect("B24 - 4,2 - Porygon (♀) - Placida - Ponderazione - 31.31.31.31.31.1 - Buio - ")) #relaxed
        self.assertTrue(iv.is_perfect("B08 - 1,4 - Furfrou (♀) - Scaltra - Foltopelo - 31.31.31.11.31.31 - Buio - [3345]")) #impish
        self.assertTrue(iv.is_perfect("B14 - 1,1 - Noibat (♂) - Timida - Indagine - 31.25.31.31.31.31 - Buio - [2393]")) #timid
        self.assertTrue(iv.is_perfect("B10 - 3,6 - Tirtouga (♀) - Allegra - Nuotovelox - 31.31.31.20.31.31 - Elettro - ")) #jolly
        self.assertTrue(iv.is_perfect("B14 - 5,1 - Bulbasaur (♂) - Modesta - Clorofilla - 31.11.31.31.31.31 - Buio - [3455]")) #modest
        self.assertTrue(iv.is_perfect("B14 - 5,4 - Amaura (♂) - Quieta - Pellegelo - 31.31.31.31.31.0 - Psico - [0132]")) #quiet
        self.assertTrue(iv.is_perfect("B14 - 4,5 - Goomy (♀) - Calma - Viscosità - 31.1.31.31.31.31 - Buio - [1478]")) #calm
        self.assertTrue(iv.is_perfect("B27 - 4,1 - Binacle (♀) - Vivace - Arraffalesto - 31.31.31.31.31.24 - Ghiaccio - ")) #sassy
        self.assertTrue(iv.is_perfect("B27 - 3,6 - Ditto (-) - Cauta - Scioltezza - 31.31.31.20.31.31 - Buio - ")) #careful

    def test_deu(self):
        self.assertTrue(iv.is_perfect("B14 - 4,3 - Kiesling (♂) - Mutig - Sandgewalt - 31.31.31.31.31.1 - Unlicht - [0009]")) #brave
        self.assertTrue(iv.is_perfect("B14 - 3,6 - Pam-Pam (♀) - Hart - Eisenfaust - 31.31.31.19.31.31 - Unlicht - [0814]")) #adamant
        self.assertTrue(iv.is_perfect("B14 - 3,1 - Clavion (♀) - Kühn - Zauberer - 31.4.31.31.31.31 - Drache - [3914]")) #bold
        self.assertTrue(iv.is_perfect("B24 - 4,2 - Porygon (♀) - Locker - Analyse - 31.31.31.31.31.1 - Unlicht - ")) #relaxed
        self.assertTrue(iv.is_perfect("B08 - 1,4 - Coiffwaff (♀) - Pfiffig - Fellkleid - 31.31.31.11.31.31 - Unlicht - [3345]")) #impish
        self.assertTrue(iv.is_perfect("B14 - 1,1 - eF-eM (♂) - Scheu - Schnüffler - 31.25.31.31.31.31 - Unlicht - [2393]")) #timid
        self.assertTrue(iv.is_perfect("B10 - 3,6 - Galapaflos (♀) - Froh - Wassertempo - 31.31.31.20.31.31 - Elektro - ")) #jolly
        self.assertTrue(iv.is_perfect("B14 - 5,1 - Bisasam (♂) - Mäßig - Chlorophyll - 31.11.31.31.31.31 - Unlicht - [3455]")) #modest
        self.assertTrue(iv.is_perfect("B14 - 5,4 - Amarino (♂) - Ruhig - Frostschicht - 31.31.31.31.31.0 - Psycho - [0132]")) #quiet
        self.assertTrue(iv.is_perfect("B14 - 4,5 - Viscora (♀) - Still - Viskosität - 31.1.31.31.31.31 - Unlicht - [1478]")) #calm
        self.assertTrue(iv.is_perfect("B27 - 4,1 - Bithora (♀) - Forsch - Langfinger - 31.31.31.31.31.24 - Eis - ")) #sassy
        self.assertTrue(iv.is_perfect("B27 - 3,6 - Ditto (-) - Sacht - Flexibilität - 31.31.31.20.31.31 - Unlicht - ")) #careful

    def test_esp(self):
        self.assertTrue(iv.is_perfect("B14 - 4,3 - Roggenrola (♂) - Audaz - Poder Arena - 31.31.31.31.31.1 - Siniestro - [0009]")) #brave
        self.assertTrue(iv.is_perfect("B14 - 3,6 - Pancham (♀) - Firme - Puño Férreo - 31.31.31.19.31.31 - Siniestro - [0814]")) #adamant
        self.assertTrue(iv.is_perfect("B14 - 3,1 - Klefki (♀) - Osado - Prestidigitador - 31.4.31.31.31.31 - Dragón - [3914]")) #bold
        self.assertTrue(iv.is_perfect("B24 - 4,2 - Porygon (♀) - Plácido - Cálculo Final - 31.31.31.31.31.1 - Siniestro - ")) #relaxed
        self.assertTrue(iv.is_perfect("B08 - 1,4 - Furfrou (♀) - Agitado - Pelaje Recio - 31.31.31.11.31.31 - Siniestro - [3345]")) #impish
        self.assertTrue(iv.is_perfect("B14 - 1,1 - Noibat (♂) - Miedoso - Cacheo - 31.25.31.31.31.31 - Siniestro - [2393]")) #timid
        self.assertTrue(iv.is_perfect("B10 - 3,6 - Tirtouga (♀) - Alegre - Nado Rápido - 31.31.31.20.31.31 - Eléctrico - ")) #jolly
        self.assertTrue(iv.is_perfect("B14 - 5,1 - Bulbasaur (♂) - Modesto - Clorofila - 31.11.31.31.31.31 - Siniestro - [3455]")) #modest
        self.assertTrue(iv.is_perfect("B14 - 5,4 - Amaura (♂) - Manso - Piel Helada - 31.31.31.31.31.0 - Psíquico - [0132]")) #quiet
        self.assertTrue(iv.is_perfect("B14 - 4,5 - Goomy (♀) - Sereno - Baba - 31.1.31.31.31.31 - Siniestro - [1478]")) #calm
        self.assertTrue(iv.is_perfect("B27 - 4,1 - Binacle (♀) - Grosero - Hurto - 31.31.31.31.31.24 - Hielo - ")) #sassy
        self.assertTrue(iv.is_perfect("B27 - 3,6 - Ditto (-) - Cauto - Flexibilidad - 31.31.31.20.31.31 - Siniestro - ")) #careful

    def test_kor(self):
        self.assertTrue(iv.is_perfect("B14 - 4,3 - 단굴 (♂) - 용감 - 모래의힘 - 31.31.31.31.31.1 - 악 - [0009]")) #brave
        self.assertTrue(iv.is_perfect("B14 - 3,6 - 판짱 (♀) - 고집 - 철주먹 - 31.31.31.19.31.31 - 악 - [0814]")) #adamant
        self.assertTrue(iv.is_perfect("B14 - 3,1 - 클레피 (♀) - 대담 - 매지션 - 31.4.31.31.31.31 - 드래곤 - [3914]")) #bold
        self.assertTrue(iv.is_perfect("B24 - 4,2 - 폴리곤 (♀) - 무사태평 - 애널라이즈 - 31.31.31.31.31.1 - 악 - ")) #relaxed
        self.assertTrue(iv.is_perfect("B08 - 1,4 - 트리미앙 (♀) - 장난꾸러기 - 퍼코트 - 31.31.31.11.31.31 - 악 - [3345]")) #impish
        self.assertTrue(iv.is_perfect("B14 - 1,1 - 음뱃 (♂) - 겁쟁이 - 통찰 - 31.25.31.31.31.31 - 악 - [2393]")) #timid
        self.assertTrue(iv.is_perfect("B10 - 3,6 - 프로토가 (♀) - 명랑 - 쓱쓱 - 31.31.31.20.31.31 - 전기 - ")) #jolly
        self.assertTrue(iv.is_perfect("B14 - 5,1 - 이상해씨 (♂) - 조심 - 엽록소 - 31.11.31.31.31.31 - 악 - [3455]")) #modest
        self.assertTrue(iv.is_perfect("B14 - 5,4 - 아마루스 (♂) - 냉정 - 프리즈스킨 - 31.31.31.31.31.0 - 에스퍼 - [0132]")) #quiet
        self.assertTrue(iv.is_perfect("B14 - 4,5 - 미끄메라 (♀) - 차분 - 미끈미끈 - 31.1.31.31.31.31 - 악 - [1478]")) #calm
        self.assertTrue(iv.is_perfect("B27 - 4,1 - 거북손손 (♀) - 건방 - 나쁜손버릇 - 31.31.31.31.31.24 - 얼음 - ")) #sassy
        self.assertTrue(iv.is_perfect("B27 - 3,6 - 메타몽 (-) - 신중 - 유연 - 31.31.31.20.31.31 - 악 - ")) #careful

    def test_vivillon(self):
        self.assertTrue(iv.is_perfect("B01 - 1,1 - Vivillon-High Plains (♀) - Timid - Friend Guard - 31.9.31.31.31.31 - Ghost - "))
        self.assertFalse(iv.is_perfect("B01 - 1,1 - Vivillon-High Plains (♀) - Timid - Friend Guard - 31.9.31.31.15.31 - Ghost - "))
        self.assertTrue(iv.is_perfect("B01 - 5,6 - Vivillon-Fancy (♀) - Calm - Compound Eyes - 31.1.31.31.31.31 - Bug -"))
        self.assertTrue(iv.is_perfect("B01 - 5,6 - ビビヨン-ファンシーなもよう (♀) - おだやか - ふくがん - 31.1.31.31.31.31 - むし - "))
        self.assertFalse(iv.is_perfect("B01 - 5,6 - Vivillon-Fancy (♀) - Calm - Compound Eyes - 25.31.31.17.28.16 - Bug -"))

    def test_farfetchd(self):
        self.assertTrue(iv.is_perfect("B02 - 2,2 - Farfetch’d (♂) - Jolly - Keen Eye - 31.31.31.2.31.31 - Electric - [0503]"))
        self.assertTrue(iv.is_perfect("B02 - 2,2 - Farfetch'd (♂) - Jolly - Keen Eye - 31.31.31.2.31.31 - Electric - [0503]"))


if __name__ == '__main__':
    unittest.main()
