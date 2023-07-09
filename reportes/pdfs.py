from decimal import Decimal
from io import BytesIO
from django.http import  HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import  inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from django.db.models import Sum
from django.db import models
import datetime
import locale

locale.setlocale(locale.LC_ALL, 'C') #Para heroku colocar 'C', para otro colocar 'es_VE'

basicTableStyle = TableStyle(
        [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.7, 0.7, 0.7)),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ])

headerStyle = ParagraphStyle(
            'header',
            fontSize=8,
            fontFamily='Junge',
            textTransform='uppercase'
            )

def generar_pdf(request,data,object_list,titulo):
    def primera_pagina(canvas, doc):
        width, height = A4
        canvas.saveState()
        titleStyle = ParagraphStyle(
            'title',
            fontSize=28,
            fontFamily='Junge',
            textTransform='uppercase'
        )
        
        i = Image('static/img/logoCasa.png',width=70.875,height=55.35)
        i.wrapOn(canvas,width,height)
        i.drawOn(canvas,10,780)

        header = Paragraph(reportHeader, titleStyle)
        header.wrapOn(canvas, width, height)
        header.drawOn(canvas,90,820)

        footer = Paragraph('<p>Reporte generado por Inmuebles Incaibo. </p>', headerStyle)
        footer.wrapOn(canvas, width, height)
        footer.drawOn(canvas,90,780)

        time = Paragraph(date, headerStyle)
        time.wrapOn(canvas, width, height)
        time.drawOn(canvas,505,780)

        canvas.restoreState()

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "Página %d" % (doc.page)
        canvas.drawCentredString(
            4 * inch,
            0.3 * inch,
            page_number_text + ', ' + reportHeader +', '+ date + '. ' + 'Generado por ' + request.user.get_full_name()
        )
        canvas.restoreState()

    reportHeader = titulo
    
    date = datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,pagesize=A4, topMargin=30, bottomMargin=30,)
    story = []
    fechaHeadingStyle = ParagraphStyle(
        'fechaHeading',
        fontSize=8.6,
    )
    fechaStyle = ParagraphStyle(
        'fecha',
        fontSize=6.5,
    )
    t = define_table(request, data, object_list)
    print(data)
    
    for n,x in enumerate(t):
        if type(t[n]) is Table:
            t[n].setStyle(basicTableStyle)
    story = [Spacer(0,30), *t]

    doc.build(story, 
        onFirstPage=primera_pagina,
        onLaterPages=add_footer,
    )
      
    response = HttpResponse(content_type='application/pdf')

    response.write(buff.getvalue())
    buff.close()

    return response

def define_table(request,data,object_list):
    if data == 'comprobante_cita':
        return comprobante_cita(object_list)
        
def comprobante_cita(cita):
    t = []
    t.append(Paragraph(f"<b>Número de Cita: </b>{cita.pk}"))

    t.append(Spacer(0,10))
    t.append(Paragraph(f"El presente comprobante certifica que el cliente <b>{cita.persona.nombre.title()} {cita.persona.apellido.title()}</b>" +
                       f", titular de la cédula de identidad <b>{cita.persona.cedula()}</b>, ha agendado una cita para la visita del inmueble " + 
                       f"<b>{cita.inmueble.nombre.upper()}</b>, del dueño <b>{cita.inmueble.dueno.nombre.title()} {cita.inmueble.dueno.apellido.title()}</b>" +
                       f", titular de la cédula de identidad <b>{cita.inmueble.dueno.cedula()}</b>, ubicado en el sector <b>{cita.inmueble.sector.nombre}</b>" + 
                       f", en la dirección <b>{cita.inmueble.ubicacion_detallada}</b>.", ParagraphStyle("", alignment = TA_JUSTIFY, fontSize = 12)))
    
    t.append(Spacer(0,10))
    t.append(Paragraph(f"El agente encargado del inmueble, <b>{cita.inmueble.agente.nombre.title()} {cita.inmueble.agente.apellido.title()}</b>, " +
                       f"titular de la cédula de identidad <b>{cita.inmueble.agente.cedula()}</b>, puede ser contactado por el cliente al correo " +
                       f"<b>{cita.inmueble.agente.usuario_persona.email}</b> o al número de teléfono <b>{cita.inmueble.agente.numero_telefono}</b>.",
                        ParagraphStyle("", alignment = TA_JUSTIFY, fontSize = 12) ))
    
    t.append(Spacer(0,10))
    t.append(Paragraph(f"<b>El presente comprobante debe ser llevado en este formato o en formato MP3 el día {cita.fecha_asignada.date} del mes {cita.fecha_asignada.month} del año {cita.fecha_asignada.year}," +
                       f"a las {cita.fecha_asignada.hour} horas con 00 minutos en la dirección del inmueble para la comprobación de su identidad al momento de la visita.</b>",
                       ParagraphStyle("", alignment = TA_JUSTIFY, fontSize = 12)))
    
    return t
