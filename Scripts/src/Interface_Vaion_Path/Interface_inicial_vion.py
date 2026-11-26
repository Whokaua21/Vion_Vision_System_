"""
VION VISION - Dashboard "Central de monitoramento" (PySide6)

MAPA DO CÓDIGO (procure pelas etiquetas [n] nos comentários):
  [S] STYLE ................ todas as cores e estilos (QSS)
  [C] COMPONENTES .......... VistaCamera, CartaoKpi (peças reutilizáveis)
  [1] SIDEBAR .............. menu lateral esquerdo
  [2] BARRA SUPERIOR ....... unidade, data/hora, busca, sino
  [3] CABEÇALHO DA PÁGINA .. título + botão "Exportar resumo"
  [4] CARTÕES KPI .......... 4 cartões de números
  [5] MONITORAMENTO AO VIVO  grade 2x2 de câmeras
  [6] RELATÓRIO INTELIGENTE  cartão roxo à direita das câmeras
  [7] OCORRÊNCIAS RECENTES . tabela inferior
  [8] RODAPÉ ............... sincronização e créditos

Imagens opcionais (pasta assets/ ao lado deste arquivo):
  cam01.jpg, cam04.jpg, cam08.jpg, cam12.jpg
Sem elas, cada câmera mostra um fundo escuro de placeholder.
"""

import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QButtonGroup,
    QSizePolicy,
)
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QPixmap, QPainterPath, QPen, QFont
from PySide6.QtCore import Qt, QRectF, QTimer


# ----------------------------------------------------------------------
# CONFIGURAÇÕES FÁCEIS DE EDITAR
# ----------------------------------------------------------------------
MARCA = "VION VISION"
SUBMARCA = "INTELLIGENT SECURITY"
PASTA_ASSETS = Path(__file__).parent / "assets"
MESES = ["jan.", "fev.", "mar.", "abr.", "mai.", "jun.",
         "jul.", "ago.", "set.", "out.", "nov.", "dez."]


# ----------------------------------------------------------------------
# [S] STYLE - cores e estilos de todos os componentes
# ----------------------------------------------------------------------
STYLE = """
QWidget { font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif; }
QWidget#janela   { background-color: #0B0D1A; }
QWidget#conteudo { background-color: #0B0D1A; }
QScrollArea      { border: none; background: transparent; }
QScrollBar:vertical { background: transparent; width: 8px; margin: 0; }
QScrollBar::handle:vertical { background: #2A2F55; border-radius: 4px; min-height: 30px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

/* ---------- [1] SIDEBAR ---------- */
QFrame#sidebar { background-color: #0D1020; border-right: 1px solid #1A1E38; }
QLabel#logo     { color: #FFFFFF; font-size: 13px; }
QLabel#logo_sub { color: #7E81A3; font-size: 7px; }
QFrame#workspace { background-color: #151933; border: 1px solid #22274A; border-radius: 10px; }
QLabel#ws_rotulo { color: #7E81A3; font-size: 8px; }
QLabel#ws_nome   { color: #FFFFFF; font-size: 12px; font-weight: 600; }
QLabel#ws_seta   { color: #9A9CB8; font-size: 12px; }
QLabel#secao     { color: #7E81A3; font-size: 9px; }
QPushButton#nav_item {
    background: transparent; border: none; border-radius: 8px;
    color: #A9ABC8; font-size: 12px; text-align: left; padding-left: 12px;
}
QPushButton#nav_item:hover   { background-color: #151933; color: #FFFFFF; }
QPushButton#nav_item:checked { background-color: #2A2552; color: #FFFFFF; }
QLabel#nav_badge {
    background-color: rgba(255, 90, 110, 45); color: #FF7A88;
    border-radius: 4px; padding: 1px 5px; font-size: 9px; font-weight: 700;
}
QFrame#status_ia { background-color: #0F1328; border: 1px solid #1E2342; border-radius: 10px; }
QLabel#status_titulo { color: #34D399; font-size: 10px; font-weight: 600; }
QLabel#status_desc   { color: #7E81A3; font-size: 9px; }
QPushButton#btn_config {
    background: transparent; border: none; color: #A9ABC8;
    font-size: 12px; text-align: left; padding-left: 8px;
}
QPushButton#btn_config:hover { color: #FFFFFF; }
QLabel#avatar {
    background-color: #2A2F55; color: #FFFFFF; border-radius: 16px;
    font-size: 11px; font-weight: 700;
}
QLabel#usuario_nome  { color: #FFFFFF; font-size: 11px; font-weight: 600; }
QLabel#usuario_cargo { color: #7E81A3; font-size: 9px; }

/* ---------- [2] BARRA SUPERIOR ---------- */
QFrame#topbar { background-color: #0B0D1A; border-bottom: 1px solid #1A1E38; }
QPushButton#btn_unidade {
    background: transparent; border: none; color: #E4E5F2;
    font-size: 12px; font-weight: 600; padding: 6px 4px;
}
QPushButton#btn_unidade:hover { color: #FFFFFF; }
QLabel#data_hora { color: #7E81A3; font-size: 10px; }
QLabel#chip_ambiente {
    background-color: #151933; border: 1px solid #22274A; border-radius: 10px;
    color: #C9CBE6; font-size: 10px; padding: 4px 10px;
}
QPushButton#btn_icone {
    background: transparent; border: none; color: #A9ABC8; font-size: 15px;
    min-width: 30px; max-width: 30px; min-height: 30px; max-height: 30px;
}
QPushButton#btn_icone:hover { color: #FFFFFF; background-color: #151933; border-radius: 8px; }

/* ---------- [3] CABEÇALHO DA PÁGINA ---------- */
QLabel#pagina_titulo    { color: #FFFFFF; font-size: 24px; font-weight: 700; }
QLabel#pagina_subtitulo { color: #9A9CB8; font-size: 12px; }
QPushButton#btn_exportar {
    background-color: #12152A; border: 1px solid #262B4F; border-radius: 10px;
    color: #E4E5F2; font-size: 12px; font-weight: 600; padding: 10px 16px;
}
QPushButton#btn_exportar:hover { background-color: #1A1E3A; }

/* ---------- [4] CARTÕES KPI ---------- */
QFrame#kpi { background-color: #12152A; border: 1px solid #1E2240; border-radius: 12px; }
QLabel#kpi_titulo  { color: #C9CBE6; font-size: 11px; }
QLabel#kpi_icone   { font-size: 14px; }
QLabel#kpi_valor   { color: #FFFFFF; font-size: 30px; font-weight: 700; }
QLabel#kpi_sufixo  { color: #7E81A3; font-size: 13px; padding-bottom: 4px; }
QLabel#kpi_nota    { color: #7E81A3; font-size: 10px; }
QLabel#kpi_nota_critica { color: #FF7A88; font-size: 10px; }

/* ---------- [5] MONITORAMENTO AO VIVO ---------- */
QLabel#secao_titulo { color: #FFFFFF; font-size: 15px; font-weight: 700; }
QLabel#secao_contador { color: #7E81A3; font-size: 11px; }
QPushButton#btn_filtro {
    background-color: #12152A; border: 1px solid #262B4F; border-radius: 8px;
    color: #E4E5F2; font-size: 11px; font-weight: 600; padding: 7px 12px;
}
QPushButton#btn_filtro:hover { background-color: #1A1E3A; }
QPushButton#btn_grade {
    background-color: #12152A; border: 1px solid #262B4F; border-radius: 8px;
    color: #A79CFA; font-size: 13px; min-width: 32px; max-width: 32px;
    min-height: 30px; max-height: 30px;
}
QFrame#cam_card { background-color: #12152A; border: 1px solid #262B4F; border-radius: 12px; }
QFrame#cam_card[critica="true"] { border: 1px solid #C0394B; }
QLabel#cam_tag, QLabel#cam_hora, QLabel#cam_expandir {
    background-color: rgba(8, 10, 24, 165); border-radius: 6px;
    color: #FFFFFF; font-size: 9px; font-weight: 600; padding: 3px 7px;
}
QLabel#cam_nome { color: #FFFFFF; font-size: 12px; font-weight: 600; }
QLabel#cam_sub  { color: #7E81A3; font-size: 9px; }
QLabel#legenda  { color: #7E81A3; font-size: 10px; }

/* selos Crítica / Atenção / Normal (usados na tela toda) */
QLabel#badge { border-radius: 6px; padding: 3px 8px; font-size: 10px; font-weight: 600; }
QLabel#badge[tipo="critica"] {
    color: #FF7A88; background-color: rgba(255, 90, 110, 38);
    border: 1px solid rgba(255, 90, 110, 110);
}
QLabel#badge[tipo="atencao"] {
    color: #F5B544; background-color: rgba(245, 181, 68, 30);
    border: 1px solid rgba(245, 181, 68, 100);
}
QLabel#badge[tipo="normal"] {
    color: #34D399; background-color: rgba(52, 211, 153, 28);
    border: 1px solid rgba(52, 211, 153, 90);
}

/* ---------- [6] RELATÓRIO INTELIGENTE ---------- */
QFrame#relatorio {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #231E52, stop:1 #15183A);
    border: 1px solid #30367A; border-radius: 14px;
}
QLabel#rel_titulo_card { color: #FFFFFF; font-size: 13px; font-weight: 600; }
QLabel#rel_chip_ia {
    background-color: rgba(124, 108, 242, 60); border-radius: 6px;
    color: #C9C2FF; font-size: 9px; font-weight: 700; padding: 3px 8px;
}
QLabel#rel_hora   { color: #9A9CB8; font-size: 10px; }
QLabel#rel_titulo { color: #FFFFFF; font-size: 20px; font-weight: 700; }
QLabel#rel_texto  { color: #C9CBE6; font-size: 12px; }
QFrame#rel_detalhes { background-color: rgba(8, 10, 30, 110); border: 1px solid #2A2F66; border-radius: 10px; }
QLabel#det_rotulo { color: #9A9CB8; font-size: 10px; }
QLabel#det_valor  { color: #FFFFFF; font-size: 10px; font-weight: 600; }
QLabel#det_valor_atencao { color: #F5B544; font-size: 10px; font-weight: 600; }
QLabel#rel_reco   { color: #C9CBE6; font-size: 11px; }
QLabel#rel_reco_icone { color: #A79CFA; font-size: 13px; }
QPushButton#btn_relatorio {
    background-color: #7C6CF2; color: #FFFFFF; border: none; border-radius: 10px;
    padding: 12px; font-size: 12px; font-weight: 600;
}
QPushButton#btn_relatorio:hover   { background-color: #8D7FF7; }
QPushButton#btn_relatorio:pressed { background-color: #6A5BDD; }
QLabel#rel_nota { color: #7E81A3; font-size: 9px; }

/* ---------- [7] OCORRÊNCIAS RECENTES ---------- */
QFrame#card { background-color: #12152A; border: 1px solid #1E2240; border-radius: 12px; }
QLabel#card_titulo { color: #FFFFFF; font-size: 14px; font-weight: 700; }
QLabel#chip_abertas {
    background-color: rgba(245, 181, 68, 30); border: 1px solid rgba(245, 181, 68, 100);
    border-radius: 6px; color: #F5B544; font-size: 10px; font-weight: 600; padding: 3px 8px;
}
QPushButton#btn_ver_todas { background: transparent; border: none; color: #A79CFA; font-size: 11px; font-weight: 600; }
QPushButton#btn_ver_todas:hover { color: #FFFFFF; }
QLabel#th { color: #7E81A3; font-size: 9px; font-weight: 600; }
QLabel#td { color: #E4E5F2; font-size: 11px; }
QLabel#td_ok { color: #34D399; font-size: 11px; }
QLabel#linha_titulo { color: #FFFFFF; font-size: 12px; font-weight: 600; }
QLabel#linha_sub    { color: #7E81A3; font-size: 9px; }
QLabel#chevron      { color: #7E81A3; font-size: 16px; }
QFrame#linha_sep    { background-color: #1E2240; }

/* ---------- [8] RODAPÉ ---------- */
QLabel#rodape { color: #6F7296; font-size: 10px; }
"""


# ----------------------------------------------------------------------
# FUNÇÕES AUXILIARES (atalhos para criar widgets repetidos)
# ----------------------------------------------------------------------
def label(texto, nome, espaco=0.0, quebra=False):
    """QLabel com objectName (para o QSS) e espaçamento opcional entre letras."""
    lbl = QLabel(texto)
    lbl.setObjectName(nome)
    if espaco:
        fonte = lbl.font()
        fonte.setLetterSpacing(QFont.AbsoluteSpacing, espaco)
        lbl.setFont(fonte)
    lbl.setWordWrap(quebra)
    return lbl


def badge(tipo):
    """Selo colorido. tipo: 'critica', 'atencao' ou 'normal'."""
    textos = {"critica": "◉  Crítica", "atencao": "△  Atenção", "normal": "✓  Normal"}
    lbl = QLabel(textos[tipo])
    lbl.setObjectName("badge")
    lbl.setProperty("tipo", tipo)          # o QSS escolhe a cor por esta propriedade
    lbl.setAlignment(Qt.AlignCenter)
    return lbl


def separador():
    """Linha horizontal fina."""
    linha = QFrame()
    linha.setObjectName("linha_sep")
    linha.setFixedHeight(1)
    return linha


def data_hora_topo():
    d = datetime.now()
    return f"{d.day:02d} {MESES[d.month - 1]} {d.year}, {d:%H:%M:%S}"


# ----------------------------------------------------------------------
# [C] COMPONENTE: VistaCamera - imagem da câmera + etiquetas por cima
# ----------------------------------------------------------------------
class VistaCamera(QWidget):
    def __init__(self, cam_id, cor_base, imagem=None, deteccao=None):
        """
        cam_id   : texto da etiqueta, ex. "CAM 01"
        cor_base : cor do placeholder (usada quando não há imagem)
        imagem   : nome do arquivo dentro de assets/ (opcional)
        deteccao : (x, y, largura, altura, texto) em frações 0-1 -> caixa vermelha da IA
        """
        super().__init__()
        self.cor_base = QColor(cor_base)
        self.deteccao = deteccao
        caminho = PASTA_ASSETS / imagem if imagem else None
        self.pix = QPixmap(str(caminho)) if caminho and caminho.exists() else QPixmap()
        self.setMinimumHeight(140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 10, 10, 10)

        # Linha de cima: etiqueta "AO VIVO · CAM xx" e ícone de expandir
        topo = QHBoxLayout()
        tag = QLabel(f"<span style='color:#34D399'>●</span> AO VIVO  "
                     f"<span style='color:#9A9CB8'>{cam_id}</span>")
        tag.setObjectName("cam_tag")
        topo.addWidget(tag)
        topo.addStretch()
        topo.addWidget(label("⤢", "cam_expandir"))
        lay.addLayout(topo)
        lay.addStretch()

        # Linha de baixo: data/hora (atualizada pelo relógio)
        base = QHBoxLayout()
        self.lbl_hora = label("", "cam_hora")
        base.addWidget(self.lbl_hora)
        base.addStretch()
        lay.addLayout(base)

    def set_hora(self, texto):
        self.lbl_hora.setText(f"▢  {texto}")

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Recorte: só os cantos de cima são arredondados
        caminho = QPainterPath()
        caminho.addRoundedRect(QRectF(0, 0, w, h + 24), 11, 11)
        p.setClipPath(caminho)

        if not self.pix.isNull():
            esc = self.pix.scaled(self.size(), Qt.KeepAspectRatioByExpanding,
                                  Qt.SmoothTransformation)
            p.drawPixmap(-((esc.width() - w) // 2), -((esc.height() - h) // 2), esc)
        else:
            grad = QLinearGradient(0, 0, 0, h)
            grad.setColorAt(0.0, self.cor_base.lighter(130))
            grad.setColorAt(1.0, self.cor_base.darker(160))
            p.fillRect(self.rect(), grad)
            p.setPen(QPen(QColor(255, 255, 255, 12), 1))      # linhas tipo "grade"
            for i in range(1, 6):
                p.drawLine(0, int(h * i / 6), w, int(h * i / 6))

        if self.deteccao:                                      # caixa de detecção da IA
            fx, fy, fw, fh, texto = self.deteccao
            ret = QRectF(w * fx, h * fy, w * fw, h * fh)
            p.setPen(QPen(QColor("#FF5A6E"), 1.5))
            p.setBrush(Qt.NoBrush)
            p.drawRect(ret)
            p.setBrush(QColor("#FF5A6E"))
            p.setPen(Qt.NoPen)
            p.drawRect(QRectF(ret.left(), ret.top() - 14, 62, 14))
            p.setPen(QColor("white"))
            fonte = p.font()
            fonte.setPointSize(7)
            p.setFont(fonte)
            p.drawText(QRectF(ret.left(), ret.top() - 14, 62, 14), Qt.AlignCenter, texto)


# ----------------------------------------------------------------------
# [C] COMPONENTE: CartaoKpi - cartão de número grande
# ----------------------------------------------------------------------
class CartaoKpi(QFrame):
    def __init__(self, titulo, icone, cor_icone, valor, sufixo="", nota="", nota_critica=False):
        super().__init__()
        self.setObjectName("kpi")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(0)

        # Linha de cima: título + ícone colorido
        topo = QHBoxLayout()
        topo.addWidget(label(titulo, "kpi_titulo"))
        topo.addStretch()
        icone_lbl = label(icone, "kpi_icone")
        icone_lbl.setStyleSheet(f"color: {cor_icone};")
        topo.addWidget(icone_lbl)
        lay.addLayout(topo)
        lay.addSpacing(8)

        # Número grande + sufixo (ex.: "/ 24")
        linha = QHBoxLayout()
        linha.setSpacing(6)
        linha.addWidget(label(valor, "kpi_valor"), alignment=Qt.AlignBottom)
        if sufixo:
            linha.addWidget(label(sufixo, "kpi_sufixo"), alignment=Qt.AlignBottom)
        linha.addStretch()
        lay.addLayout(linha)
        lay.addSpacing(6)

        # Nota pequena embaixo (vermelha quando crítica)
        lay.addWidget(label(nota, "kpi_nota_critica" if nota_critica else "kpi_nota"))


# ----------------------------------------------------------------------
# JANELA PRINCIPAL
# ----------------------------------------------------------------------
class Dashboard_Vion_Vision(QWidget):
    def __init__(self):
        super().__init__()
        self.cameras = []                      # guarda as câmeras para atualizar a hora
        self.montar_tela()

        # Relógio: atualiza hora do topo, das câmeras e do rodapé a cada segundo
        self.relogio = QTimer(self)
        self.relogio.timeout.connect(self._atualizar_relogio)
        self.relogio.start(1000)
        self._atualizar_relogio()

    def montar_tela(self):
        self.setWindowTitle("Central de monitoramento | Beta")
        self.setObjectName("janela")
        self.setMinimumSize(1240, 780)
        self.resize(1400, 880)
        self.setStyleSheet(STYLE)

        raiz = QHBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        raiz.setSpacing(0)

        # Coluna esquerda: sidebar [1]
        raiz.addWidget(self._criar_sidebar())

        # Coluna direita: barra superior [2] + área rolável com o conteúdo
        direita = QVBoxLayout()
        direita.setSpacing(0)
        direita.addWidget(self._criar_topbar())

        area = QScrollArea()
        area.setWidgetResizable(True)
        area.setFrameShape(QFrame.NoFrame)
        conteudo = QWidget()
        conteudo.setObjectName("conteudo")
        conteudo.setAttribute(Qt.WA_StyledBackground, True)
        col = QVBoxLayout(conteudo)
        col.setContentsMargins(28, 22, 28, 18)
        col.setSpacing(0)

        col.addLayout(self._criar_cabecalho_pagina())     # [3]
        col.addSpacing(18)
        col.addLayout(self._criar_kpis())                 # [4]
        col.addSpacing(22)

        # Faixa do meio: câmeras [5] à esquerda e relatório [6] à direita
        meio = QHBoxLayout()
        meio.setSpacing(16)
        meio.addLayout(self._criar_monitoramento(), stretch=2)
        meio.addWidget(self._criar_relatorio(), stretch=1)
        col.addLayout(meio)
        col.addSpacing(20)

        col.addWidget(self._criar_ocorrencias())          # [7]
        col.addSpacing(14)
        col.addLayout(self._criar_rodape())               # [8]

        area.setWidget(conteudo)
        direita.addWidget(area)
        raiz.addLayout(direita, stretch=1)

    # ==================================================================
    # [1] SIDEBAR - menu lateral
    # ==================================================================
    def _criar_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)
        lay = QVBoxLayout(sidebar)
        lay.setContentsMargins(14, 20, 14, 14)
        lay.setSpacing(0)

        # --- Logo ---
        lay.addWidget(label(MARCA, "logo", 3))
        lay.addSpacing(2)
        lay.addWidget(label(SUBMARCA, "logo_sub", 1.8))
        lay.addSpacing(22)

        # --- Seletor de espaço de trabalho ---
        ws = QFrame()
        ws.setObjectName("workspace")
        ws_lay = QHBoxLayout(ws)
        ws_lay.setContentsMargins(12, 9, 12, 9)
        textos = QVBoxLayout()
        textos.setSpacing(2)
        textos.addWidget(label("ESPAÇO DE TRABALHO", "ws_rotulo", 0.8))
        textos.addWidget(label("Grupo Horizonte", "ws_nome"))
        ws_lay.addLayout(textos)
        ws_lay.addStretch()
        ws_lay.addWidget(label("⌄", "ws_seta"))
        lay.addWidget(ws)
        lay.addSpacing(20)

        # --- Itens do menu ---
        lay.addWidget(label("OPERAÇÃO", "secao", 1.2))
        lay.addSpacing(8)
        self.grupo_nav = QButtonGroup(self)       # garante que só um item fique ativo
        itens = [
            ("▦", "Visão geral", None),
            ("◉", "Câmeras", None),
            ("△", "Ocorrências", "6"),            # terceiro valor = selo de contagem
            ("▤", "Relatórios IA", None),
            ("☺", "Pessoas e acessos", None),
            ("⌂", "Unidades", None),
        ]
        for i, (icone, texto, selo) in enumerate(itens):
            btn = self._criar_item_nav(icone, texto, selo)
            btn.setChecked(i == 0)                # "Visão geral" começa ativo
            lay.addWidget(btn)
            lay.addSpacing(3)

        lay.addStretch()

        # --- Status da IA ---
        status = QFrame()
        status.setObjectName("status_ia")
        st_lay = QVBoxLayout(status)
        st_lay.setContentsMargins(12, 10, 12, 10)
        st_lay.setSpacing(3)
        st_lay.addWidget(label("●  IA operacional", "status_titulo"))
        st_lay.addWidget(label("Monitoramento contínuo • 24/7", "status_desc"))
        lay.addWidget(status)
        lay.addSpacing(12)

        # --- Configurações ---
        btn_cfg = QPushButton("⚙   Configurações")
        btn_cfg.setObjectName("btn_config")
        btn_cfg.setCursor(Qt.PointingHandCursor)
        btn_cfg.setFixedHeight(32)
        lay.addWidget(btn_cfg)
        lay.addSpacing(10)
        lay.addWidget(separador())
        lay.addSpacing(12)

        # --- Usuário logado ---
        usuario = QHBoxLayout()
        usuario.setSpacing(10)
        avatar = label("AM", "avatar")
        avatar.setFixedSize(32, 32)
        avatar.setAlignment(Qt.AlignCenter)
        usuario.addWidget(avatar)
        dados = QVBoxLayout()
        dados.setSpacing(1)
        dados.addWidget(label("Ana Martins", "usuario_nome"))
        dados.addWidget(label("Supervisora de segurança", "usuario_cargo"))
        usuario.addLayout(dados)
        usuario.addStretch()
        lay.addLayout(usuario)

        return sidebar

    def _criar_item_nav(self, icone, texto, selo=None):
        """Botão do menu. Se 'selo' for informado, mostra a bolinha de contagem à direita."""
        btn = QPushButton(f"{icone}    {texto}")
        btn.setObjectName("nav_item")
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(36)
        if selo:
            lay = QHBoxLayout(btn)
            lay.setContentsMargins(0, 0, 10, 0)
            lay.addStretch()
            lbl = QLabel(selo)
            lbl.setObjectName("nav_badge")
            lbl.setAttribute(Qt.WA_TransparentForMouseEvents)   # o clique vai para o botão
            lay.addWidget(lbl)
        self.grupo_nav.addButton(btn)
        return btn

    # ==================================================================
    # [2] BARRA SUPERIOR
    # ==================================================================
    def _criar_topbar(self):
        barra = QFrame()
        barra.setObjectName("topbar")
        barra.setFixedHeight(56)
        lay = QHBoxLayout(barra)
        lay.setContentsMargins(28, 0, 20, 0)
        lay.setSpacing(12)

        # Seletor de unidade (esquerda)
        btn_unidade = QPushButton("▣   CD Horizonte · Unidade São Paulo    ⌄")
        btn_unidade.setObjectName("btn_unidade")
        btn_unidade.setCursor(Qt.PointingHandCursor)
        lay.addWidget(btn_unidade)
        lay.addStretch()

        # Data/hora, chip de ambiente, busca e notificações (direita)
        self.lbl_data_hora = label("", "data_hora")
        lay.addWidget(self.lbl_data_hora)
        lay.addWidget(label("◉  Ambiente demonstrativo", "chip_ambiente"))
        for icone in ("⌕", "🔔"):
            btn = QPushButton(icone)
            btn.setObjectName("btn_icone")
            btn.setCursor(Qt.PointingHandCursor)
            lay.addWidget(btn)
        return barra

    # ==================================================================
    # [3] CABEÇALHO DA PÁGINA
    # ==================================================================
    def _criar_cabecalho_pagina(self):
        lay = QHBoxLayout()
        textos = QVBoxLayout()
        textos.setSpacing(4)
        textos.addWidget(label("Central de monitoramento", "pagina_titulo"))
        textos.addWidget(label("Sua operação, sob uma visão inteligente.", "pagina_subtitulo"))
        lay.addLayout(textos)
        lay.addStretch()

        btn = QPushButton("⤓   Exportar resumo")
        btn.setObjectName("btn_exportar")
        btn.setCursor(Qt.PointingHandCursor)
        lay.addWidget(btn, alignment=Qt.AlignTop)
        return lay

    # ==================================================================
    # [4] CARTÕES KPI
    # ==================================================================
    def _criar_kpis(self):
        lay = QHBoxLayout()
        lay.setSpacing(14)
        lay.addWidget(CartaoKpi("Câmeras online", "▣", "#34D399", "22", "/ 24",
                                "2 offline · verificar conexão"))
        lay.addWidget(CartaoKpi("Ocorrências hoje", "△", "#F5B544", "08", "",
                                "4 abertas · 4 resolvidas"))
        lay.addWidget(CartaoKpi("Prioridade crítica", "◉", "#FF7A88", "01", "",
                                "Acesso não autorizado", nota_critica=True))
        lay.addWidget(CartaoKpi("Relatórios IA", "▤", "#A79CFA", "12", "",
                                "Último gerado às 14:31"))
        return lay

    # ==================================================================
    # [5] MONITORAMENTO AO VIVO - grade 2x2 de câmeras
    # ==================================================================
    def _criar_monitoramento(self):
        lay = QVBoxLayout()
        lay.setSpacing(0)

        # --- Cabeçalho: título, contador, filtro e botão de grade ---
        cab = QHBoxLayout()
        cab.setSpacing(8)
        cab.addWidget(label("Monitoramento ao vivo", "secao_titulo"))
        cab.addWidget(label("4 de 24", "secao_contador"))
        cab.addStretch()
        filtro = QPushButton("⌄   Todas as áreas")
        filtro.setObjectName("btn_filtro")
        filtro.setCursor(Qt.PointingHandCursor)
        cab.addWidget(filtro)
        grade_btn = QPushButton("▦")
        grade_btn.setObjectName("btn_grade")
        grade_btn.setCursor(Qt.PointingHandCursor)
        cab.addWidget(grade_btn)
        lay.addLayout(cab)
        lay.addSpacing(12)

        # --- Grade 2x2 --- (para trocar as câmeras, edite esta lista)
        # (id, nome, descrição, status, cor placeholder, imagem, caixa de detecção)
        cameras = [
            ("CAM 01", "Portaria principal", "CAM 01 · Acesso de colaboradores",
             "critica", "#2B3350", "cam01.jpg", (0.62, 0.30, 0.18, 0.55, "Pessoa · 98%")),
            ("CAM 04", "Galpão de expedição", "CAM 04 · Operação logística",
             "normal", "#2E3138", "cam04.jpg", None),
            ("CAM 08", "Docas de carga", "CAM 08 · Área operacional",
             "atencao", "#3A3F4A", "cam08.jpg", None),
            ("CAM 12", "Estacionamento", "CAM 12 · Perímetro externo",
             "normal", "#262B33", "cam12.jpg", None),
        ]
        grade = QGridLayout()
        grade.setSpacing(12)
        for i, (cid, nome, desc, status, cor, img, det) in enumerate(cameras):
            grade.addWidget(self._criar_cartao_camera(cid, nome, desc, status, cor, img, det),
                            i // 2, i % 2)
        grade.setRowStretch(0, 1)
        grade.setRowStretch(1, 1)
        lay.addLayout(grade, stretch=1)
        lay.addSpacing(10)

        # --- Legenda embaixo ---
        legenda = QHBoxLayout()
        legenda.addWidget(label("⌁  Transmissão protegida · Atualização em tempo real", "legenda"))
        legenda.addStretch()
        legenda.addWidget(label("HD · 1080p", "legenda"))
        lay.addLayout(legenda)
        return lay

    def _criar_cartao_camera(self, cid, nome, desc, status, cor, img, deteccao):
        card = QFrame()
        card.setObjectName("cam_card")
        card.setProperty("critica", status == "critica")      # borda vermelha se crítica
        lay = QVBoxLayout(card)
        lay.setContentsMargins(1, 1, 1, 1)
        lay.setSpacing(0)

        vista = VistaCamera(cid, cor, img, deteccao)
        self.cameras.append(vista)
        lay.addWidget(vista, stretch=1)

        # Faixa de informação embaixo da imagem
        info = QHBoxLayout()
        info.setContentsMargins(12, 10, 12, 10)
        textos = QVBoxLayout()
        textos.setSpacing(2)
        textos.addWidget(label(nome, "cam_nome"))
        textos.addWidget(label(desc, "cam_sub"))
        info.addLayout(textos)
        info.addStretch()
        info.addWidget(badge(status), alignment=Qt.AlignVCenter)
        lay.addLayout(info)
        return card

    # ==================================================================
    # [6] RELATÓRIO INTELIGENTE
    # ==================================================================
    def _criar_relatorio(self):
        card = QFrame()
        card.setObjectName("relatorio")
        card.setMinimumWidth(300)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 16, 18, 14)
        lay.setSpacing(0)

        # --- Cabeçalho: título do cartão + chip "IA" ---
        cab = QHBoxLayout()
        cab.addWidget(label("✦  Relatório Inteligente", "rel_titulo_card"))
        cab.addStretch()
        cab.addWidget(label("✧ IA", "rel_chip_ia"))
        lay.addLayout(cab)
        lay.addSpacing(14)

        # --- Horário e selo "Crítica · Revisão necessária" ---
        lay.addWidget(label("◷  Hoje, 14:31 · Últimos 30 minutos", "rel_hora"))
        lay.addSpacing(10)
        selo = badge("critica")
        selo.setText("◉  Crítica · Revisão necessária")
        lay.addWidget(selo, alignment=Qt.AlignLeft)
        lay.addSpacing(12)

        # --- Título e descrição do alerta ---
        lay.addWidget(label("Acesso não autorizado na portaria principal", "rel_titulo",
                            quebra=True))
        lay.addSpacing(10)
        lay.addWidget(label(
            "A IA identificou uma pessoa sem credencial reconhecida na área restrita "
            "às 14:28. A ocorrência foi encaminhada à supervisão.",
            "rel_texto", quebra=True))
        lay.addSpacing(14)

        # --- Caixa de detalhes (Classificação / Responsável / Acompanhamento) ---
        det = QFrame()
        det.setObjectName("rel_detalhes")
        det_lay = QGridLayout(det)
        det_lay.setContentsMargins(14, 10, 14, 10)
        det_lay.setVerticalSpacing(8)
        linhas = [("Classificação", "Controle de acesso", "det_valor"),
                  ("Responsável", "Ana Martins", "det_valor"),
                  ("Acompanhamento", "Em análise", "det_valor_atencao")]
        for r, (rot, val, estilo) in enumerate(linhas):
            det_lay.addWidget(label(rot, "det_rotulo"), r, 0)
            det_lay.addWidget(label(val, estilo), r, 1, Qt.AlignRight)
        lay.addWidget(det)
        lay.addSpacing(12)

        # --- Recomendação ---
        reco = QHBoxLayout()
        reco.setSpacing(8)
        reco.addWidget(label("🛡", "rel_reco_icone"), alignment=Qt.AlignTop)
        reco.addWidget(label("Recomendação: validar a identificação com a equipe da portaria.",
                             "rel_reco", quebra=True), stretch=1)
        lay.addLayout(reco)

        lay.addStretch()

        # --- Botão principal e nota final ---
        btn = QPushButton("↗   Abrir relatório completo")
        btn.setObjectName("btn_relatorio")
        btn.setCursor(Qt.PointingHandCursor)
        lay.addWidget(btn)
        lay.addSpacing(10)
        nota = label("Análise assistida por IA. Validação humana necessária.", "rel_nota")
        lay.addWidget(nota)
        return card

    # ==================================================================
    # [7] OCORRÊNCIAS RECENTES - tabela
    # ==================================================================
    def _criar_ocorrencias(self):
        card = QFrame()
        card.setObjectName("card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # --- Cabeçalho do cartão ---
        cab = QHBoxLayout()
        cab.setContentsMargins(18, 16, 18, 12)
        cab.setSpacing(10)
        cab.addWidget(label("Ocorrências recentes", "card_titulo"))
        cab.addWidget(label("△  4 abertas", "chip_abertas"))
        cab.addStretch()
        ver = QPushButton("Ver todas →")
        ver.setObjectName("btn_ver_todas")
        ver.setCursor(Qt.PointingHandCursor)
        cab.addWidget(ver)
        lay.addLayout(cab)
        lay.addWidget(separador())

        # --- Dados da tabela --- (para adicionar linhas, edite esta lista)
        # (ocorrência, local, prioridade, status, responsável, horário)
        dados = [
            ("Acesso não autorizado", "Portaria principal · CAM 01",
             "critica", "Em análise", "Ana Martins", "14:28"),
            ("Ausência de EPI", "Docas de carga · CAM 08",
             "atencao", "Encaminhada", "Carlos Lima", "14:16"),
            ("Permanência em área restrita", "Galpão de expedição · CAM 04",
             "atencao", "Em análise", "Ana Martins", "13:52"),
            ("Reconhecimento facial validado", "Portaria principal · CAM 01",
             "normal", "Resolvida", "Equipe da portaria", "13:40"),
        ]

        grade = QGridLayout()
        grade.setContentsMargins(18, 0, 18, 0)
        grade.setHorizontalSpacing(12)
        grade.setVerticalSpacing(0)
        for coluna, peso in enumerate((5, 2, 2, 2, 1, 0)):    # largura relativa das colunas
            grade.setColumnStretch(coluna, peso)

        # Linha de títulos das colunas
        for c, titulo in enumerate(("OCORRÊNCIA / LOCAL", "PRIORIDADE", "STATUS",
                                    "RESPONSÁVEL", "HORÁRIO")):
            th = label(titulo, "th", 0.8)
            th.setMinimumHeight(34)
            grade.addWidget(th, 0, c)
        grade.addWidget(separador(), 1, 0, 1, 6)

        # Linhas de dados (cada ocorrência usa 2 linhas da grade: conteúdo + separador)
        r = 2
        for i, (titulo, local, prio, status, resp, hora) in enumerate(dados):
            celula = QWidget()                                 # coluna 0: título + local
            cel_lay = QVBoxLayout(celula)
            cel_lay.setContentsMargins(0, 0, 0, 0)
            cel_lay.setSpacing(2)
            cel_lay.addStretch()
            cel_lay.addWidget(label(titulo, "linha_titulo"))
            cel_lay.addWidget(label(local, "linha_sub"))
            cel_lay.addStretch()
            celula.setMinimumHeight(56)
            grade.addWidget(celula, r, 0)

            grade.addWidget(badge(prio), r, 1, Qt.AlignLeft | Qt.AlignVCenter)  # prioridade

            st = label(status, "td_ok" if status == "Resolvida" else "td")      # status
            grade.addWidget(st, r, 2)
            grade.addWidget(label(resp, "td"), r, 3)                            # responsável
            grade.addWidget(label(hora, "td"), r, 4)                            # horário
            grade.addWidget(label("›", "chevron"), r, 5)                        # seta

            if i < len(dados) - 1:
                grade.addWidget(separador(), r + 1, 0, 1, 6)
            r += 2
        lay.addLayout(grade)
        return card

    # ==================================================================
    # [8] RODAPÉ
    # ==================================================================
    def _criar_rodape(self):
        lay = QHBoxLayout()
        self.lbl_sync = label("", "rodape")
        lay.addWidget(self.lbl_sync)
        lay.addStretch()
        lay.addWidget(label(f"Dados ilustrativos · {MARCA} © {datetime.now().year}", "rodape"))
        return lay

    # ==================================================================
    # RELÓGIO - atualiza todos os textos de hora
    # ==================================================================
    def _atualizar_relogio(self):
        agora = datetime.now()
        self.lbl_data_hora.setText(data_hora_topo())                         # [2]
        for cam in self.cameras:                                             # [5]
            cam.set_hora(agora.strftime("%d/%m/%Y %H:%M:%S"))
        self.lbl_sync.setText(f"⟳  Sincronizado às {agora:%H:%M:%S}")       # [8]

janela_dashboard = None

def app():
    global janela_dashboard

    instancia = QApplication.instance()

    if instancia is None:
        instancia = QApplication(sys.argv)

    janela_dashboard = Dashboard_Vion_Vision()
    janela_dashboard.show()

    if instancia is not QApplication.instance():
        return

    if len(sys.argv) >= 0 and instancia is not None:
        if instancia is not None and instancia.thread() == janela_dashboard.thread():
            if instancia.applicationName() == "":
                instancia.setApplicationName("Vion Vision")

    if instancia is not None and not hasattr(instancia, "_executando"):
        instancia._executando = True
        instancia.exec()