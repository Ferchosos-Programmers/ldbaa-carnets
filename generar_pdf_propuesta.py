import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0F172A"))
        
        # Header (Top)
        self.drawString(15 * mm, 285 * mm, "LIGA DEPORTIVA BARRIAL ARGELIA ALTA (LDBAA)")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(195 * mm, 285 * mm, "PROPUESTA OFICIAL: LIGABET 2026")
        
        # Top Rule
        self.setStrokeColor(colors.HexColor("#2ECC71"))
        self.setLineWidth(1.5)
        self.line(15 * mm, 282 * mm, 195 * mm, 282 * mm)
        
        # Bottom Rule
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(15 * mm, 15 * mm, 195 * mm, 15 * mm)
        
        # Footer
        self.setFont("Helvetica", 7.5)
        self.drawString(15 * mm, 11 * mm, "Plataforma Tecnológica LDBAA | Sistema de Autogestión Financiera y Pronósticos")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(195 * mm, 11 * mm, page_text)
        self.restoreState()


def generate_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A")
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6,
        spaceBefore=10
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#166534"),
        spaceAfter=4,
        spaceBefore=6
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0F172A")
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0F172A")
    )

    tbl_header = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )

    tbl_cell_center = ParagraphStyle(
        'TblCellCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B"),
        alignment=1
    )

    tbl_cell_bold_center = ParagraphStyle(
        'TblCellBoldCenter',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        alignment=1
    )

    story = []

    # ==================== PÁGINA 1: PORTADA & RESUMEN EJECUTIVO ====================
    # Banner Box
    banner_data = [
        [
            Paragraph("<font color='#2ECC71' size='9'><b>PROPUESTA DE INNOVACIÓN & AUTOGESTIÓN 2026</b></font>", body_style),
        ],
        [
            Paragraph("<font color='#FFFFFF' size='18'><b>LIGABET: SISTEMA DE PRONÓSTICOS DEPORTIVOS</b></font><br/><font color='#94A3B8' size='9.5'>Apuestas Partido a Partido con Modelo de Cero Riesgo Financiero para la LDBAA</font>", body_style),
        ]
    ]
    banner_table = Table(banner_data, colWidths=[180 * mm])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LINELEFT', (0,0), (-1,-1), 4, colors.HexColor("#2ECC71")),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 4 * mm))

    # Meta Grid (Destinatario, Modelo, Pagos)
    meta_data = [
        [
            Paragraph("<b>DESTINATARIO:</b><br/>Directiva Central y Delegados de Clubes LDBAA", tbl_cell),
            Paragraph("<b>MODELO ECONÓMICO:</b><br/>70% Premios Ganadores / 30% Caja Liga", tbl_cell),
            Paragraph("<b>MÉTODO DE PAGO:</b><br/>DeUna QR / Transferencia / Efectivo", tbl_cell),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[60 * mm, 60 * mm, 60 * mm])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 5 * mm))

    # Sección 1
    story.append(Paragraph("1. Resumen Ejecutivo y Objetivos de la Propuesta", h1_style))
    p1 = ("La plataforma <b>LigaBet</b> es una iniciativa tecnológica de autogestión financiera diseñada "
          "específicamente para la <b>Liga Deportiva Barrial Argelia Alta</b>. Permite a los hinchas, familiares "
          "y delegados apostar al resultado de los partidos de cada fin de semana (Local, Empate o Visita) "
          "desde su celular mediante transferencias rápidas de <b>DeUna</b>.")
    story.append(Paragraph(p1, body_style))
    story.append(Spacer(1, 2.5 * mm))
    
    p2 = ("<b>Principio de Cero Riesgo:</b> A diferencia de una casa de apuestas comercial que puede perder dinero, "
          "LigaBet funciona bajo un <b>Pozo Acumulado (Pari-Mutuel) por Partido</b>. La Liga nunca gasta ni arriesga su "
          "propio dinero: el <b>30% del total recaudado queda automáticamente como ganancia neta para la Liga</b>, y el "
          "<b>70% restante se reparte íntegramente entre los apostadores que acertaron</b>.")
    story.append(Paragraph(p2, body_style))
    story.append(Spacer(1, 4 * mm))

    # 3 Pilares
    story.append(Paragraph("2. Pilares Estratégicos del Proyecto", h1_style))
    pilares_data = [
        [
            Paragraph("<font color='#15803D'><b>🛡️ Cero Riesgo Financiero</b></font><br/><font size='7.5' color='#334155'>La Liga no paga cuotas de su bolsillo. Los premios salen exclusivamente del 70% de las apuestas del mismo partido.</font>", tbl_cell),
            Paragraph("<font color='#15803D'><b>⚽ Partido a Partido</b></font><br/><font size='7.5' color='#334155'>No se obliga al hincha a adivinar 10 partidos. Apuesta directamente al encuentro de su equipo favorito con montos desde $1.</font>", tbl_cell),
            Paragraph("<font color='#15803D'><b>📅 Auditoría los Martes</b></font><br/><font size='7.5' color='#334155'>Las apuestas entran de inmediato el fin de semana, pero la revisión bancaria y pago oficial se realiza los martes en sesión.</font>", tbl_cell),
        ]
    ]
    pilares_table = Table(pilares_data, colWidths=[58 * mm, 58 * mm, 58 * mm])
    pilares_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BBF7D0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BBF7D0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(pilares_table)

    story.append(PageBreak())

    # ==================== PÁGINA 2: MATEMÁTICA Y CASOS DE ESTUDIO ====================
    story.append(Paragraph("3. Modelo Matemático: ¿Cómo se calculan los premios?", h1_style))
    
    formula_text = (
        "<b>FÓRMULAS OFICIALES POR CADA ENCUENTRO:</b><br/>"
        "• <b>Recaudación Total</b> = Suma de apuestas a (Local + Empate + Visita)<br/>"
        "• <b>Ganancia Neta Liga (30%)</b> = Recaudación Total × 0.30<br/>"
        "• <b>Bolsa de Premios Ganadores (70%)</b> = Recaudación Total × 0.70<br/>"
        "• <b>Premio por cada $1 apostado</b> = Bolsa de Premios (70%) ÷ Total apostado a la opción ganadora"
    )
    formula_data = [[Paragraph(formula_text, tbl_cell)]]
    formula_table = Table(formula_data, colWidths=[180 * mm])
    formula_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.white),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINELEFT', (0,0), (-1,-1), 4, colors.HexColor("#F1C40F")),
    ]))
    # Adjust text color inside formula
    formula_data[0][0] = Paragraph(f"<font color='#F8FAFC'>{formula_text}</font>", tbl_cell)
    story.append(formula_table)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("4. Caso de Estudio Práctico (Demostración con $15 Recaudados)", h1_style))
    p_caso = ("Supongamos el partido de la fecha: <b>Arsenal (Local) vs. Juventus (Visita)</b> con 15 apuestas de $1.00:")
    story.append(Paragraph(p_caso, body_style))
    story.append(Spacer(1, 2 * mm))

    # Box de datos del partido
    match_info_data = [
        [
            Paragraph("<b>Opción 1: Local (Arsenal)</b><br/>10 personas ($10.00)", tbl_cell_center),
            Paragraph("<b>Opción X: Empate</b><br/>0 personas ($0.00)", tbl_cell_center),
            Paragraph("<b>Opción 2: Visita (Juventus)</b><br/>5 personas ($5.00)", tbl_cell_center),
            Paragraph("<b>REPARTO FIJO:</b><br/>🏦 Liga (30%): $4.50<br/>🏆 Premios (70%): $10.50", tbl_cell_center),
        ]
    ]
    match_info_tbl = Table(match_info_data, colWidths=[45 * mm, 40 * mm, 45 * mm, 50 * mm])
    match_info_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(match_info_tbl)
    story.append(Spacer(1, 3 * mm))

    # Tabla de Resultados según quién gane
    res_table_data = [
        [
            Paragraph("Escenario de Resultado", tbl_header),
            Paragraph("Ganadores", tbl_header),
            Paragraph("Cálculo de Reparto", tbl_header),
            Paragraph("Premio c/u ($1)", tbl_header),
            Paragraph("Ganancia de la Liga", tbl_header),
        ],
        [
            Paragraph("<b>🟢 Gana Arsenal (Local)</b><br/><font size='7' color='#64748B'>Ganó el equipo favorito</font>", tbl_cell),
            Paragraph("10 personas ($10)", tbl_cell_center),
            Paragraph("$10.50 ÷ $10.00 apostados", tbl_cell_center),
            Paragraph("<b>$1.05</b><br/><font size='6.5' color='#16A34A'>Recupera $1 + $0.05</font>", tbl_cell_bold_center),
            Paragraph("<b>$4.50</b> (30% limpio)", tbl_cell_center),
        ],
        [
            Paragraph("<b>🔴 Gana Juventus (Visita)</b><br/><font size='7' color='#64748B'>Ganó el equipo sorpresa</font>", tbl_cell),
            Paragraph("5 personas ($5)", tbl_cell_center),
            Paragraph("$10.50 ÷ $5.00 apostados", tbl_cell_center),
            Paragraph("<b>$2.10</b><br/><font size='6.5' color='#16A34A'>¡Duplica su dinero!</font>", tbl_cell_bold_center),
            Paragraph("<b>$4.50</b> (30% limpio)", tbl_cell_center),
        ],
        [
            Paragraph("<b>🟡 Quedan Empatados</b><br/><font size='7' color='#64748B'>Nadie apostó al empate</font>", tbl_cell),
            Paragraph("0 personas ($0)", tbl_cell_center),
            Paragraph("Pozo Desierto", tbl_cell_center),
            Paragraph("<b>$0.00</b>", tbl_cell_bold_center),
            Paragraph("<b>$15.00</b> (100% Liga)", tbl_cell_center),
        ]
    ]
    res_table = Table(res_table_data, colWidths=[48 * mm, 32 * mm, 40 * mm, 30 * mm, 30 * mm])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(res_table)
    story.append(Spacer(1, 5 * mm))

    # Sección 5: Proyección Financiera Mensual
    story.append(Paragraph("5. Proyección de Ingresos Netos para la Liga (LDBAA)", h1_style))
    
    proj_data = [
        [
            Paragraph("Volumen de Apuestas por Fecha", tbl_header),
            Paragraph("Recaudación", tbl_header),
            Paragraph("🏆 Premios Hinchas (70%)", tbl_header),
            Paragraph("🏦 Ganancia Liga (30%)", tbl_header),
            Paragraph("Ingreso Mensual (4 Fechas)", tbl_header),
        ],
        [
            Paragraph("50 apuestas de $2.00", tbl_cell),
            Paragraph("$100.00", tbl_cell_center),
            Paragraph("$70.00", tbl_cell_center),
            Paragraph("<b>$30.00</b>", tbl_cell_center),
            Paragraph("<b>$120.00 / mes</b>", tbl_cell_bold_center),
        ],
        [
            Paragraph("150 apuestas de $2.00", tbl_cell),
            Paragraph("$300.00", tbl_cell_center),
            Paragraph("$210.00", tbl_cell_center),
            Paragraph("<b>$90.00</b>", tbl_cell_center),
            Paragraph("<b>$360.00 / mes</b>", tbl_cell_bold_center),
        ],
        [
            Paragraph("<b>300 apuestas de $2.00</b>", tbl_cell),
            Paragraph("<b>$600.00</b>", tbl_cell_center),
            Paragraph("$420.00", tbl_cell_center),
            Paragraph("<font color='#16A34A'><b>$180.00</b></font>", tbl_cell_center),
            Paragraph("<font color='#15803D'><b>$720.00 / mes</b></font>", tbl_cell_bold_center),
        ]
    ]
    proj_table = Table(proj_data, colWidths=[48 * mm, 28 * mm, 38 * mm, 32 * mm, 34 * mm])
    proj_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(proj_table)

    story.append(PageBreak())

    # ==================== PÁGINA 3: OPERACIÓN, PAGOS Y SEGURIDAD ====================
    story.append(Paragraph("6. Flujo de Operación y Pagos (DeUna & Sesión de Martes)", h1_style))
    
    pasos_data = [
        [
            Paragraph("<b>1</b>", tbl_cell_bold_center),
            Paragraph("<b>Selección y Pago en la Web (LigaBet):</b><br/><font size='7.5' color='#475569'>El usuario entra desde su celular a ligabet.html, escoge el partido, la opción deseada (Local/Empate/Visita), escanea el QR de DeUna oficial y digita el monto apostado.</font>", tbl_cell)
        ],
        [
            Paragraph("<b>2</b>", tbl_cell_bold_center),
            Paragraph("<b>Generación Instantánea de Ticket:</b><br/><font size='7.5' color='#475569'>Para no generar cuellos de botella en fin de semana, el usuario ingresa su Nombre, WhatsApp y N° de Comprobante DeUna. El sistema emite inmediatamente su <b>Ticket Activo (ej: BET-482)</b>.</font>", tbl_cell)
        ],
        [
            Paragraph("<b>3</b>", tbl_cell_bold_center),
            Paragraph("<b>Cierre Automático con Vocalía Digital:</b><br/><font size='7.5' color='#475569'>Al iniciar el partido en cancha, el sistema bloquea nuevas apuestas para ese encuentro. Cuando el vocal finaliza el partido en <code>vocalias.html</code>, el sistema marca automáticamente a los ganadores.</font>", tbl_cell)
        ],
        [
            Paragraph("<b>4</b>", tbl_cell_bold_center),
            Paragraph("<b>Auditoría y Pago Oficial en Sesión de los Martes:</b><br/><font size='7.5' color='#475569'>El día martes, el Tesorero ingresa al panel <code>ligabet-admin.html</code>, verifica los extractos de DeUna y entrega o transfiere los premios oficiales a los ganadores legítimos.</font>", tbl_cell)
        ],
    ]
    pasos_table = Table(pasos_data, colWidths=[10 * mm, 170 * mm])
    pasos_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor("#2ECC71")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(pasos_table)
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("7. Reglas de Transparencia y Casos Especiales", h1_style))
    seg_data = [
        [
            Paragraph("<b>🔒 Blindaje contra Comprobantes Falsos</b><br/><font size='7.5' color='#475569'>Si algún usuario ingresa un número de comprobante falso, el tesorero lo detecta el martes al revisar la cuenta de DeUna. Ese ticket queda automáticamente <b>ANULADO</b>.</font>", tbl_cell),
            Paragraph("<b>🌧️ Partidos Suspendidos o Cancelados</b><br/><font size='7.5' color='#475569'>Si un encuentro no se juega por lluvia o incidentes, el sistema <b>devuelve el 100% del dinero apostado</b> a cada hincha el día martes sin penalizaciones.</font>", tbl_cell),
        ]
    ]
    seg_table = Table(seg_data, colWidths=[88 * mm, 88 * mm])
    seg_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(seg_table)
    story.append(Spacer(1, 6 * mm))

    # Conclusión
    conc_data = [[
        Paragraph("<font color='#166534'><b>CONCLUSIÓN:</b> La implementación de LigaBet representa un hito de modernización y autogestión para la <b>Liga Barrial Argelia Alta</b>. Genera ingresos limpios semanales para la Liga, no arriesga un solo centavo de su caja y ofrece a los hinchas una experiencia emocionante e interactiva.</font>", tbl_cell)
    ]]
    conc_table = Table(conc_data, colWidths=[180 * mm])
    conc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86EFAC")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(conc_table)
    story.append(Spacer(1, 10 * mm))

    # Firmas
    firmas_data = [
        [
            Paragraph("____________________________<br/><b>Comisión Técnica Digital</b><br/><font size='7' color='#64748B'>Desarrollo & Plataforma LDBAA</font>", tbl_cell_center),
            Paragraph("____________________________<br/><b>Directiva Central LDBAA</b><br/><font size='7' color='#64748B'>Presidente / Secretario</font>", tbl_cell_center),
            Paragraph("____________________________<br/><b>Tesorería General</b><br/><font size='7' color='#64748B'>Control Financiero</font>", tbl_cell_center),
        ]
    ]
    firmas_table = Table(firmas_data, colWidths=[60 * mm, 60 * mm, 60 * mm])
    firmas_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(firmas_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado con exito: {output_filename}")

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "Propuesta_Oficial_LigaBet_LDBAA.pdf")
    generate_pdf(output_path)
