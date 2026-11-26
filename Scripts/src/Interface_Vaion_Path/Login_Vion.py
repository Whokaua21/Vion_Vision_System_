import re
import sys
from datetime import date
from pathlib import Path
from . import Interface_inicial_vion 

# 'c:\Users\Klaus\Documents\Vion_Vision_System\Scripts\python.exe' 'c:/Users/Klaus/Documents/Vion_Vision_System/Scripts/src/Interface_Vaion_Path/Login_Vaion.py'
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtGui import (
    QPainter,
    QLinearGradient,
    QColor,
    QPixmap,
    QPainterPath,
    QPen,
    QFont,
)
from PySide6.QtCore import (
    Qt,
    QEvent,
    QPointF,
    QRectF,
    QPoint,
    QPropertyAnimation,
    QEasingCurve,
)


# ----------------------------------------------------------------------
# Configurações do protótipo
# ----------------------------------------------------------------------
MARCA = "VION VISION"                       # troque aqui se o nome for outro
SUBMARCA = "INTELLIGENT SECURITY"
EMAIL_TESTE = "demo@empresa.com"            # credenciais fixas só para o protótipo
SENHA_TESTE = "1234"
IMAGEM_HERO = Path(__file__).parent / "img" / "Banner_Vaion_Vision_Log.png"   # foto do cartão (opcional)
print(IMAGEM_HERO)
COR_ACENTO = "#7C6CF2"


STYLE = """
QWidget#Vaion_Login { background-color: #0A0C18; }
QLabel, QCheckBox, QPushButton, QLineEdit {
    font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
}

/* ============ PAINEL ESQUERDO ============ */
QLabel#logo        { color: #FFFFFF; font-size: 22px; font-weight: 400; }
QLabel#logo_sub    { color: #A7A3D6; font-size: 9px; }
QFrame#traco       { background-color: #8E83F5; }
QLabel#eyebrow     { color: #A79CFA; font-size: 10px; font-weight: 600; }
QLabel#headline    { color: #FFFFFF; font-size: 38px; font-weight: 500; }
QLabel#descricao   { color: #C9C7EC; font-size: 14px; }
QLabel#rodape_esq  { color: #8D89C4; font-size: 10px; }

/* cartão hero */
QLabel#chip {
    background-color: rgba(10, 12, 30, 150);
    border: 1px solid rgba(255, 255, 255, 40);
    border-radius: 10px;
    color: #E6E4FA;
    font-size: 11px;
    padding: 5px 10px;
}
QFrame#hero_info {
    background-color: rgba(10, 12, 30, 170);
    border: 1px solid rgba(255, 255, 255, 35);
    border-radius: 10px;
}
QLabel#hero_titulo { color: #FFFFFF; font-size: 13px; font-weight: 700; background: transparent; }
QLabel#hero_desc   { color: #B9B6E0; font-size: 10px; background: transparent; }
QFrame#hero_barra {
    background-color: rgba(10, 12, 30, 215);
    border-top: 1px solid rgba(255, 255, 255, 30);
    border-bottom-left-radius: 14px;
    border-bottom-right-radius: 14px;
}
QLabel#hero_item { color: #D7D5F3; font-size: 11px; background: transparent; }

/* ============ PAINEL DIREITO ============ */
QWidget#painel_login { background-color: #0A0C18; }
QLabel#ajuda      { color: #9A9CB8; font-size: 11px; }
QLabel#eyebrow2   { color: #8E83F5; font-size: 10px; font-weight: 600; }
QLabel#titulo     { color: #FFFFFF; font-size: 26px; font-weight: 600; }
QLabel#subtitulo  { color: #9A9CB8; font-size: 13px; }
QLabel#rotulo     { color: #E4E5F2; font-size: 12px; font-weight: 600; }

QFrame#campo_box {
    background-color: #12152A;
    border: 1px solid #232744;
    border-radius: 10px;
}
QFrame#campo_box[foco="true"] { border: 1px solid #7C6CF2; }
QLabel#campo_icone { color: #7E81A3; font-size: 14px; background: transparent; }
QLineEdit#campo_input {
    background: transparent;
    border: none;
    color: #E8E9F5;
    font-size: 13px;
    padding: 13px 0px;
    selection-background-color: #7C6CF2;
}
QPushButton#btn_olho {
    background: transparent;
    border: none;
    color: #7E81A3;
    font-size: 11px;
    padding: 0px 4px;
}
QPushButton#btn_olho:hover { color: #FFFFFF; }

QCheckBox { color: #B3B5CE; font-size: 12px; spacing: 8px; }
QCheckBox::indicator {
    width: 15px; height: 15px;
    border-radius: 4px;
    border: 1px solid #3A3F66;
    background: #12152A;
}
QCheckBox::indicator:checked { background: #7C6CF2; border: 1px solid #7C6CF2; }

QPushButton#btn_link {
    background: transparent; border: none;
    color: #9A8FFA; font-size: 12px;
}
QPushButton#btn_link:hover { color: #FFFFFF; }

QLabel#mensagem { font-size: 12px; min-height: 16px; }

QPushButton#btn_entrar {
    background-color: #7C6CF2;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 13px;
    font-size: 13px;
    font-weight: 600;
}
QPushButton#btn_entrar:hover   { background-color: #8D7FF7; }
QPushButton#btn_entrar:pressed { background-color: #6A5BDD; }

QFrame#linha  { background-color: #232744; }
QLabel#ou     { color: #7E81A3; font-size: 11px; }

QPushButton#btn_sso {
    background-color: #12152A;
    color: #E4E5F2;
    border: 1px solid #232744;
    border-radius: 10px;
    padding: 12px;
    font-size: 12px;
    font-weight: 500;
}
QPushButton#btn_sso:hover { background-color: #1A1E3A; border: 1px solid #343A66; }
QLabel#dica_sso { color: #7E81A3; font-size: 10px; }

QFrame#aviso {
    background-color: #0F1223;
    border: 1px solid #1B1F38;
    border-radius: 10px;
}
QLabel#aviso_icone { color: #8E83F5; font-size: 13px; background: transparent; }
QLabel#aviso_texto { color: #9A9CB8; font-size: 10px; background: transparent; }

QPushButton#rodape_link {
    background: transparent; border: none;
    color: #7E81A3; font-size: 10px;
}
QPushButton#rodape_link:hover { color: #FFFFFF; }
"""


def criar_label(texto, nome, espaco=0.0, quebra=False):
    lbl = QLabel(texto)
    lbl.setObjectName(nome)
    if espaco:
        fonte = lbl.font()
        fonte.setLetterSpacing(QFont.AbsoluteSpacing, espaco)
        lbl.setFont(fonte)
    lbl.setWordWrap(quebra)
    return lbl


# ----------------------------------------------------------------------
# Componentes
# ----------------------------------------------------------------------
class PainelDegrade(QWidget):
    """Fundo com degradê índigo e círculos translúcidos (painel esquerdo)."""

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        grad = QLinearGradient(0, h, w, 0)
        grad.setColorAt(0.0, QColor("#0D0B2A"))
        grad.setColorAt(0.55, QColor("#241C6E"))
        grad.setColorAt(1.0, QColor("#3F34AD"))
        p.fillRect(self.rect(), grad)

        p.setPen(Qt.NoPen)
        p.setBrush(QColor(255, 255, 255, 14))
        raio = w * 0.55
        p.drawEllipse(QPointF(w * 0.98, h * 0.0), raio, raio)
        p.setBrush(QColor(255, 255, 255, 8))
        p.drawEllipse(QPointF(w * 0.12, h * 1.02), raio * 0.6, raio * 0.6)


class CartaoHero(QWidget):
    """Cartão com imagem (ou degradê, se não houver imagem) e elementos por cima."""

    def __init__(self):
        super().__init__()
        self.setMinimumHeight(50)
        self.pix = QPixmap(str(IMAGEM_HERO)) if IMAGEM_HERO.exists() else QPixmap()


    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        caminho = QPainterPath()
        caminho.addRoundedRect(QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5), 14, 14)
        p.setClipPath(caminho)

        if not self.pix.isNull():
            esc = self.pix.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            x = (esc.width() - self.width()) // 2
            y = (esc.height() - self.height()) // 2
            p.drawPixmap(-x, -y, esc)
        else:
            grad = QLinearGradient(0, 0, self.width(), self.height())
            grad.setColorAt(0.0, QColor("#1B2A5C"))
            grad.setColorAt(1.0, QColor("#0B1030"))
            p.fillRect(self.rect(), grad)

        p.setClipping(False)
        p.setPen(QPen(QColor(255, 255, 255, 45), 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(caminho)


class Campo(QFrame):
    """Campo com ícone à esquerda e (opcional) botão de mostrar/ocultar senha."""

    def __init__(self, icone, placeholder, senha=False):
        super().__init__()
        self.setObjectName("campo_box")
        self.setProperty("foco", False)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 0, 10, 0)
        lay.setSpacing(10)

        lay.addWidget(criar_label(icone, "campo_icone"))

        self.input = QLineEdit()
        self.input.setObjectName("campo_input")
        self.input.setPlaceholderText(placeholder)
        self.input.installEventFilter(self)
        lay.addWidget(self.input)

        if senha:
            self.input.setEchoMode(QLineEdit.Password)
            self.btn_olho = QPushButton("Mostrar")
            self.btn_olho.setObjectName("btn_olho")
            self.btn_olho.setCheckable(True)
            self.btn_olho.setCursor(Qt.PointingHandCursor)
            self.btn_olho.toggled.connect(self._alternar)
            lay.addWidget(self.btn_olho)

    def _alternar(self, visivel):
        self.input.setEchoMode(QLineEdit.Normal if visivel else QLineEdit.Password)
        self.btn_olho.setText("Ocultar" if visivel else "Mostrar")

    def _set_foco(self, valor):
        self.setProperty("foco", valor)
        self.style().unpolish(self)
        self.style().polish(self)

    def eventFilter(self, obj, ev):
        if obj is self.input:
            if ev.type() == QEvent.FocusIn:
                self._set_foco(True)
            elif ev.type() == QEvent.FocusOut:
                self._set_foco(False)
        return super().eventFilter(obj, ev)


# ----------------------------------------------------------------------
# Janela principal
# ----------------------------------------------------------------------
class Interface_Vaion_Vision(QWidget):
    def __init__(self):
        super().__init__()
        self._fade_feito = False
        self.Login_Vaion_Vision()

    def Login_Vaion_Vision(self):
        self.setWindowTitle("Login | Beta")
        self.setObjectName("Vaion_Login")
        self.setMinimumSize(1100, 720)
        self.setStyleSheet(STYLE)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.box_info = self._criar_painel_info()
        self.log_vaion = self._criar_painel_login()

        layout.addWidget(self.box_info)
        layout.addWidget(self.log_vaion)
        layout.setStretch(0, 8)
        layout.setStretch(1, 7)

    # ------------------------- painel esquerdo -------------------------
    def _criar_painel_info(self):
        painel = PainelDegrade()
        painel.setObjectName("box_info")

        lay = QVBoxLayout(painel)
        lay.setContentsMargins(56, 46, 56, 30)
        lay.setSpacing(0)

        lay.addWidget(criar_label(MARCA, "logo", 5))
        lay.addSpacing(4)
        lay.addWidget(criar_label(SUBMARCA, "logo_sub", 2.5))
        lay.addSpacing(46)

        eyebrow = QHBoxLayout()
        eyebrow.setSpacing(10)
        traco = QFrame()
        traco.setObjectName("traco")
        traco.setFixedSize(22, 2)
        eyebrow.addWidget(traco, alignment=Qt.AlignVCenter)
        eyebrow.addWidget(criar_label("INTELIGÊNCIA QUE PROTEGE", "eyebrow", 1.5))
        eyebrow.addStretch()
        lay.addLayout(eyebrow)
        lay.addSpacing(18)

        lay.addWidget(criar_label("Antecipe riscos.\nProteja o que importa.", "headline"))
        lay.addSpacing(16)
        lay.addWidget(
            criar_label(
                "Câmeras, inteligência artificial e decisões mais rápidas. "
                "Toda a sua segurança em uma única visão.",
                "descricao",
                quebra=True,
            )
        )
        lay.addSpacing(34)

        lay.addWidget(CartaoHero(), stretch=1)
        lay.addSpacing(30)

        rodape = QHBoxLayout()
        rodape.addWidget(criar_label(f"{MARCA} © {date.today().year}", "rodape_esq"))
        rodape.addStretch()
        rodape.addWidget(criar_label("Tecnologia a serviço da segurança.", "rodape_esq"))
        lay.addLayout(rodape)

        return painel

    # ------------------------- painel direito -------------------------
    def _criar_painel_login(self):
        painel = QWidget()
        painel.setObjectName("painel_login")
        painel.setAttribute(Qt.WA_StyledBackground, True)

        raiz = QVBoxLayout(painel)
        raiz.setContentsMargins(40, 28, 40, 26)

        # Ajuda no topo
        
        topo = QHBoxLayout()
        topo.addStretch()
        topo.addWidget(criar_label("ⓘ  Precisa de ajuda?", "ajuda"))
        raiz.addLayout(topo)
        raiz.addStretch()

        # Formulário centralizado
        form_widget = QWidget()
        form_widget.setFixedWidth(470)
        form = QVBoxLayout(form_widget)
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(0)

        form.addWidget(criar_label("ACESSO EMPRESARIAL", "eyebrow2", 1.5))
        form.addSpacing(10)
        form.addWidget(criar_label("Bem-vindo de volta", "titulo"))
        form.addSpacing(8)
        form.addWidget(
            criar_label("Entre para acompanhar sua operação com segurança.", "subtitulo")
        )
        form.addSpacing(26)

        # E-mail
        form.addWidget(criar_label("E-mail corporativo", "rotulo"))
        form.addSpacing(8)
        self.campo_email = Campo("", "seu.nome@empresa.com.br")
        form.addWidget(self.campo_email)
        form.addSpacing(18)

        # Senha
        form.addWidget(criar_label("Senha", "rotulo"))
        form.addSpacing(8)
        self.campo_senha = Campo("", "Digite sua senha", senha=True)
        form.addWidget(self.campo_senha)
        form.addSpacing(14)

        # Manter conectado / esqueci a senha
        opcoes = QHBoxLayout()
        self.chk_manter = QCheckBox("Manter conectado")
        self.chk_manter.setChecked(True)
        self.btn_esqueci = QPushButton("Esqueci minha senha")
        self.btn_esqueci.setObjectName("btn_link")
        self.btn_esqueci.setCursor(Qt.PointingHandCursor)
        self.btn_esqueci.clicked.connect(
            lambda: self._mostrar_mensagem("Recuperação de senha ainda não implementada.")
        )
        opcoes.addWidget(self.chk_manter)
        opcoes.addStretch()
        opcoes.addWidget(self.btn_esqueci)
        form.addLayout(opcoes)
        form.addSpacing(10)

        # Mensagem
        self.lbl_mensagem = QLabel("")
        self.lbl_mensagem.setObjectName("mensagem")
        form.addWidget(self.lbl_mensagem)
        form.addSpacing(6)

        # Botão principal
        self.btn_entrar = QPushButton("Entrar na plataforma")
        self.btn_entrar.setObjectName("btn_entrar")
        self.btn_entrar.setCursor(Qt.PointingHandCursor)
        self.btn_entrar.clicked.connect(self._tentar_login)
        form.addWidget(self.btn_entrar)
        form.addSpacing(18)

        # Divisor "ou"
        divisor = QHBoxLayout()
        divisor.setSpacing(12)
        linha1, linha2 = QFrame(), QFrame()
        for linha in (linha1, linha2):
            linha.setObjectName("linha")
            linha.setFixedHeight(1)
        divisor.addWidget(linha1)
        divisor.addWidget(criar_label("ou", "ou"))
        divisor.addWidget(linha2)
        form.addLayout(divisor)
        form.addSpacing(18)

        # SSO
        self.btn_sso = QPushButton("▦   Entrar com SSO empresarial")
        self.btn_sso.setObjectName("btn_sso")
        self.btn_sso.setCursor(Qt.PointingHandCursor)
        self.btn_sso.clicked.connect(
            lambda: self._mostrar_mensagem("SSO ainda não configurado neste protótipo.")
        )
        form.addWidget(self.btn_sso)
        form.addSpacing(8)
        dica = criar_label("Use o provedor de identidade da sua organização.", "dica_sso")
        dica.setAlignment(Qt.AlignHCenter)
        form.addWidget(dica)
        form.addSpacing(22)

        # Aviso de segurança
        aviso = QFrame()
        aviso.setObjectName("aviso")
        aviso_lay = QHBoxLayout(aviso)
        aviso_lay.setContentsMargins(14, 12, 14, 12)
        aviso_lay.setSpacing(10)
        aviso_lay.addWidget(
            criar_label(
                "Acesso restrito a usuários autorizados. "
                "Sua sessão é protegida e auditada.",
                "aviso_texto",
                quebra=True,
            ),
            stretch=1,
        )
        form.addWidget(aviso)

        centro = QHBoxLayout()
        centro.addStretch()
        centro.addWidget(form_widget)
        centro.addStretch()
        raiz.addLayout(centro)
        raiz.addStretch()

        # Rodapé
        rodape = QHBoxLayout()
        rodape.addStretch()
        for texto in ("Política de privacidade", "Termos de uso"):
            btn = QPushButton(texto)
            btn.setObjectName("rodape_link")
            btn.setCursor(Qt.PointingHandCursor)
            rodape.addWidget(btn)
            rodape.addSpacing(16)
        rodape.takeAt(rodape.count() - 1)   # remove o último espaçamento
        rodape.addStretch()
        raiz.addLayout(rodape)

        # Enter: e-mail -> senha -> login
        self.campo_email.input.returnPressed.connect(self.campo_senha.input.setFocus)
        self.campo_senha.input.returnPressed.connect(self._tentar_login)

        return painel

    # ------------------------- comportamento -------------------------
    def _mostrar_mensagem(self, texto, erro=True):
        cor = "#FF6B7A" if erro else "#34D399"
        self.lbl_mensagem.setStyleSheet(f"color: {cor};")
        self.lbl_mensagem.setText(texto)

    def _tentar_login(self):
        email = self.campo_email.input.text().strip()
        senha = self.campo_senha.input.text()

        if not email or not senha:
            self._mostrar_mensagem("Informe o e-mail e a senha.")
            self._tremer_janela()
            return

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self._mostrar_mensagem("Digite um e-mail corporativo válido.")
            self._tremer_janela()
            return

        if email.lower() == EMAIL_TESTE and senha == SENHA_TESTE:
            self._mostrar_mensagem("Login realizado com sucesso!", erro=False)
            interface_vaion = Interface_inicial_vion.app()
            self.close()
            
            # Aqui você abriria a próxima tela (dashboard)
        else:
            self._mostrar_mensagem("E-mail ou senha incorretos.")
            self.campo_senha.input.clear()
            self.campo_senha.input.setFocus()
            self._tremer_janela()

    # ------------------------- animações -------------------------
    def showEvent(self, event):
        super().showEvent(event)
        if not self._fade_feito:
            self._fade_feito = True
            self.setWindowOpacity(0.0)
            self.anim_fade = QPropertyAnimation(self, b"windowOpacity")
            self.anim_fade.setDuration(600)
            self.anim_fade.setStartValue(0.0)
            self.anim_fade.setEndValue(1.0)
            self.anim_fade.setEasingCurve(QEasingCurve.OutCubic)
            self.anim_fade.start()

    def _tremer_janela(self):
        pos = self.pos()
        self.anim_shake = QPropertyAnimation(self, b"pos")
        self.anim_shake.setDuration(350)
        self.anim_shake.setKeyValueAt(0.0, pos)
        self.anim_shake.setKeyValueAt(0.2, pos + QPoint(-10, 0))
        self.anim_shake.setKeyValueAt(0.4, pos + QPoint(10, 0))
        self.anim_shake.setKeyValueAt(0.6, pos + QPoint(-6, 0))
        self.anim_shake.setKeyValueAt(0.8, pos + QPoint(6, 0))
        self.anim_shake.setKeyValueAt(1.0, pos)
        self.anim_shake.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Interface_Vaion_Vision()
    janela.show()
    sys.exit(app.exec())