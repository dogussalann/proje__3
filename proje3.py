import pygame
import sys

# Pencere ayarı
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Devre Simülatörü")
clock = pygame.time.Clock()

# Renkler
beyaz = (255, 255, 255)
siyah = (0, 0, 0)
kırmızı = (255, 0, 0)
yeşil = (0, 255, 0)
mavi = (0, 0, 255)
sarı = (255, 255, 0)
gri = (159, 182, 205)

# Buton Oluşturma ve Konumu
ve_butonu = pygame.Rect(30, 50, 135, 30)
or_butonu = pygame.Rect(30, 90, 135, 30)
not_butonu = pygame.Rect(30, 130, 135, 30)
buffer_butonu = pygame.Rect(30, 170, 135, 30)
nand_butonu = pygame.Rect(30, 210, 135, 30)
nor_butonu = pygame.Rect(30, 250, 135, 27)
xor_butonu = pygame.Rect(30, 290, 135, 29)
xnor_butonu = pygame.Rect(30, 330, 135, 30)
input_butonu = pygame.Rect(30, 420, 135, 30)
output_butonu = pygame.Rect(30, 460, 135, 30)
led_butonu = pygame.Rect(30, 500, 135, 30)
çizgi_butonu = pygame.Rect(30, 580, 135, 25)
link_butonu = pygame.Rect(30, 620, 150, 30)

# Araçlar paneli ve tasarım alanı
araç_paneli_alanı = pygame.Rect(0, 0, 300, 900)
tasarım_alanı = pygame.Rect(300, 0, 1000, 900)

# Resimleri yükleme
çalıştır_buton = pygame.image.load('resimler\\çalıştır_buton.png')
reset_buton = pygame.image.load('resimler\\reset_buton.png')
durdur_buton = pygame.image.load('resimler\\durdur_buton.png')

ve_buton = pygame.image.load('resimler\\and_buton.png')
and_gate_image = pygame.image.load('resimler\\and_gate.png')

or_buton = pygame.image.load('resimler\\or_buton.png')
or_gate_image = pygame.image.load('resimler\\or_gate.png')

not_buton = pygame.image.load('resimler\\not_buton.png')
not_gate_image = pygame.image.load('resimler\\and_gate.png')

buffer_buton = pygame.image.load('resimler\\buffer_buton.png')
buffer_gate_image = pygame.image.load('resimler\\buffer_gate.png')

nand_buton = pygame.image.load('resimler\\nand_buton.png')
nand_gate_image = pygame.image.load('resimler\\nand_gate.png')

nor_buton = pygame.image.load('resimler\\nor_buton.png')
nor_gate_image = pygame.image.load('resimler\\nor_gate.png')

xor_buton = pygame.image.load('resimler\\xor_buton.png')
xor_gate_image = pygame.image.load('resimler\\xor_gate.png')

xnor_buton = pygame.image.load('resimler\\xnor_buton.png')
xnor_gate_image = pygame.image.load('resimler\\xnor_gate.png')

input_buton = pygame.image.load('resimler\\input_buton.png')
input_gate_image = pygame.image.load('resimler\\input_gate.png')

output_buton = pygame.image.load('resimler\\output_buton.png')
output_gate_image = pygame.image.load('resimler\\output_gate.png')

led_buton = pygame.image.load('resimler\\led_buton.png')
led_gate_image = pygame.image.load('resimler\\led_gate.png')

link_buton = pygame.image.load('resimler\\link_buton.png')
link_gate_image = pygame.image.load('resimler\\link_gate.png')

çizgi_buton = pygame.image.load('resimler\\çizgi_buton.png')


# Mantık kapıları resmi ve elemanları için sınıflar
class MantıkKapısı:
    def __init__(self, gate_type, input_count):
        self.gate_type = gate_type
        self.input_count = input_count
        self.rect = pygame.Rect(0, 0, 60, 60)
        self.image = pygame.image.load(f'resimler/{gate_type.lower()}_gate.png')

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    # Mantık kapısı türüne göre çıkışlar
    def update_output(self):
        if self.label == "AND":
            self.output = all(self.inputs)

        elif self.label == "OR":
            self.output = any(self.inputs)

        elif self.label == "NOT":
            self.output = not self.inputs[0]

        elif self.label == "BUFFER":
            self.output = self.inputs[0]

        elif self.label == "NAND":
            self.output = not all(self.inputs)

        elif self.label == "NOR":
            self.output = not any(self.inputs)

        elif self.label == "XNOR":
            self.output = sum(self.inputs) % 2 == 0

        elif self.label == "XOR":
            self.output = sum(self.inputs) % 2 == 1


# Tasarımın oluşturulduğu ve renklendirlidiği bölüm
class tasarım:
    def __init__(self, label, color, is_input=True, initial_value=False):
        self.label = label
        self.color = color
        self.is_input = is_input
        self.value = initial_value
        self.rect = pygame.Rect(0, 0, 60, 60)
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.label, True, beyaz)
        screen.blit(text, self.rect.topleft)
        if not self.is_input:
            value_text = font.render(str(self.value), True, beyaz)
            screen.blit(value_text, (self.rect.x + 20, self.rect.y + 30))


# Düğüm ve Kablolar için
class Bağlantı:
    def __init__(self, baş_tasarım, son_tasarım):
        self.baş_tasarım = baş_tasarım
        self.son_tasarım = son_tasarım

    def draw(self, screen):
        başlangıç_pozisyonu = self.baş_tasarım.rect.center
        bitiş_pozisyonu = self.son_tasarım.rect.center
        pygame.draw.line(screen, siyah, başlangıç_pozisyonu, bitiş_pozisyonu, 2)


# Liste oluşturma
mantık_kapıları = []
tasarım_elemanları = []
bağlantılar = []


# Simülasyon kontrolleri ve renkleri
def draw_controls(screen):
    font = pygame.font.SysFont(None, 24)

    # Çalıştır butonu
    çalıştır_buttonu = pygame.Rect(40, 700, 115, 30)
    pygame.draw.rect(screen, yeşil, çalıştır_buttonu)
    screen.blit(çalıştır_buton, çalıştır_buttonu.topleft)

    # Reset butonu
    reset_buttonu = pygame.Rect(105, 750, 105, 30)
    pygame.draw.rect(screen, kırmızı, reset_buttonu)
    screen.blit(reset_buton, reset_buttonu.topleft)

    # Durdur butonu
    durdur_buttonu = pygame.Rect(170, 700, 105, 30)
    pygame.draw.rect(screen, sarı, durdur_buttonu)
    screen.blit(durdur_buton, durdur_buttonu.topleft)

    return çalıştır_buttonu, reset_buttonu, durdur_buttonu


# Simülasyon döngüsü
running = True
simulating = False
sürükleme = None

while running:
    screen.fill(beyaz)

    # Araçlar paneli ve başlıklar
    pygame.draw.rect(screen, gri, araç_paneli_alanı)
    font = pygame.font.SysFont(None, 24)

    text = font.render("Mantık Kapıları", True, siyah)
    screen.blit(text, (30, 15))

    text_2 = font.render("Giriş Çıkış Elemanları", True, siyah)
    screen.blit(text_2, (30, 390))

    text_3 = font.render("Bağlantı Elemanları", True, siyah)
    screen.blit(text_2, (30, 550))

    # Tasarım alanını
    pygame.draw.rect(screen, siyah, tasarım_alanı, 2)

    # Mantık kapıları ve bağlantılar
    for kapı in mantık_kapıları:
        kapı.draw(screen)
    for tasarım_elemanı in tasarım_elemanları:
        tasarım_elemanı.draw(screen)
    for bağlantı in bağlantılar:
        bağlantı.draw(screen)

    # Simülasyon kontrolleri ekleme
    çalıştır_buttonu, reset_buttonu, durdur_buttonu = draw_controls(screen)

    # Deverenin işlenmesi
    for devre in pygame.event.get():
        if devre.type == pygame.QUIT:
            running = False

        elif devre.type == pygame.MOUSEBUTTONDOWN:
            if devre.button == 1:  # Tıklama
                if ve_butonu.collidepoint(devre.pos):  # Tuşa tıklama kısmı
                    yeni_kapı = MantıkKapısı("AND", 2)  # Yeni mantık kapısı ekleme kısmı
                    yeni_kapı.rect.topleft = (400, 70)  # Yeni kapının başlangıç konumu
                    mantık_kapıları.append(yeni_kapı)  # Kapıyı oluşturma

                if or_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("OR", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                if not_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("NOT", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                if buffer_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("BUFFER", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                if nand_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("NAND", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                if nor_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("NOR", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                if xor_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("XOR", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                if xnor_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("XNOR", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                if input_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("INPUT", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                if output_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("OUTPUT", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                if led_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("LED", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                if link_butonu.collidepoint(devre.pos):
                    yeni_kapı = MantıkKapısı("LINK", 2)
                    yeni_kapı.rect.topleft = (400, 70)
                    mantık_kapıları.append(yeni_kapı)

                    # Tasarım alanı ve sürükleme
                elif tasarım_alanı.collidepoint(devre.pos):
                    for tasarım_elemanı in mantık_kapıları + tasarım_elemanları:
                        if tasarım_elemanı.rect.collidepoint(devre.pos):
                            sürükleme = tasarım_elemanı
                            break
                elif çalıştır_buttonu.collidepoint(devre.pos):  # Çalıştır-Durdur-Reset tuşlarını oluşturma
                    simulating = None
                elif durdur_buttonu.collidepoint(devre.pos):
                    simulating = False
                elif reset_buttonu.collidepoint(devre.pos):
                    mantık_kapıları.clear()


        # Tutma ve Sürükleme kısmı
        elif devre.type == pygame.MOUSEBUTTONUP:
            sürükleme = None
        elif devre.type == pygame.MOUSEMOTION:
            if sürükleme is not None:
                sürükleme.rect.topleft = devre.pos
        if simulating:
            for kapı in mantık_kapıları:
                kapı.update_output()
            for tasarım_elemanı in tasarım_elemanları:
                if not tasarım_elemanı.is_input:
                    # Çıkış elemanlarını güncelle
                    pass

    # Tuşlara kapı işlemlerinin atanması, renk ve boyutun ayarlanması
    pygame.draw.rect(screen, beyaz, ve_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("AND", True, siyah)
    screen.blit(ve_buton, ve_butonu.topleft)

    pygame.draw.rect(screen, beyaz, or_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("OR", True, siyah)
    screen.blit(or_buton, or_butonu.topleft)

    pygame.draw.rect(screen, beyaz, not_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("NOT", True, siyah)
    screen.blit(not_buton, not_butonu.topleft)

    pygame.draw.rect(screen, beyaz, buffer_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("BUFFER", True, siyah)
    screen.blit(buffer_buton, buffer_butonu.topleft)

    pygame.draw.rect(screen, beyaz, nand_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("NAND", True, siyah)
    screen.blit(nand_buton, nand_butonu.topleft)

    pygame.draw.rect(screen, beyaz, nor_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("NOR", True, siyah)
    screen.blit(nor_buton, nor_butonu.topleft)

    pygame.draw.rect(screen, beyaz, xor_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("XOR", True, siyah)
    screen.blit(xor_buton, xor_butonu.topleft)

    pygame.draw.rect(screen, beyaz, xnor_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("XNOR", True, siyah)
    screen.blit(xnor_buton, xnor_butonu.topleft)

    pygame.draw.rect(screen, beyaz, input_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("INPUT", True, siyah)
    screen.blit(input_buton, input_butonu.topleft)

    pygame.draw.rect(screen, beyaz, output_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("OUTPUT", True, siyah)
    screen.blit(output_buton, output_butonu.topleft)

    pygame.draw.rect(screen, beyaz, led_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("LED", True, siyah)
    screen.blit(led_buton, led_butonu.topleft)

    pygame.draw.rect(screen, beyaz, çizgi_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("LED", True, siyah)
    screen.blit(çizgi_buton, çizgi_butonu.topleft)

    pygame.draw.rect(screen, beyaz, link_butonu)
    font = pygame.font.Font(None, 36)
    text = font.render("LED", True, siyah)
    screen.blit(link_buton, link_butonu.topleft)

    pygame.display.flip()  # Ekranda yapılan çizimleri güncelleme
    clock.tick(50)  # Döngünün 50 FPS ile çalışmasını sağlar

# Bağlantı elemanları ve işlevleri
baş_tasarım = None

pygame.quit()
sys.exit()