from decimal import Decimal
from io import BytesIO
from django.http import  HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import  inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from django.db.models import Sum
from pagos.models import Compra
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
    elif data == 'comprobante_compra':
        return comprobante_compra(object_list)
    elif data == 'reporte_pagos':
        return reporte_pagos(request, object_list)
    elif data == 'reporte_compras':
        return reporte_compras(object_list)
    elif data == 'reporte_publicacion':
        return reporte_publicacion(object_list)
    elif data == 'reporte_cita_formalidades':
        return reporte_cita_formalidades(object_list)
        
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

def comprobante_compra(compra):
    t = []
    t.append(Paragraph(f"<b>Número de Compra: </b>{compra.pk}"))

    t.append(Spacer(0,10))
    t.append(Paragraph(f"El usuario <b>{compra.comprador}</b>, titular de la cédula de identidad <b>{compra.comprador.cedula()}</b>, "
                    +  f"ha firmado del contrato de aceptación de términos de compra del inmueble cuyos datos se muestran en la siguiente: "))
    
    t.append(Spacer(0,10))
    t.append(Table([["NOMBRE","CÓDIGO","SECTOR","UBICACIÓN", "PRECIO"],
                    [Paragraph(compra.inmueble.nombre), Paragraph(f"{compra.inmueble.pk}"), 
                     Paragraph(compra.inmueble.sector.nombre), Paragraph(compra.inmueble.ubicacion_detallada),
                     Paragraph(f"${compra.inmueble.precio}")]]))
    
    t.append(Spacer(0,10))
    t.append(Paragraph(f"Del dueño <b>{compra.inmueble.dueno}</b>, titular de la cédula de identidad <b>{compra.inmueble.dueno.cedula()}</b>."
                    +  f" Queda encargado de la presente compra el agente <b>{compra.inmueble.agente}</b>, titular de la cédula de identidad "
                    +  f"<b>{compra.inmueble.agente.cedula()}</b>, el cual puede ser contactado en las vías autorizadas: "))
    
    t.append(Spacer(0,10))
    t.append(Table([["TELÉFONO","EMAIL"],
                    [Paragraph(compra.inmueble.agente.numero_telefono), Paragraph(compra.inmueble.agente.usuario_persona.email)]]))
    
    t.append(Spacer(0,10))
    t.append(Paragraph(f"<b>Compra acordada entre las partes interesadas con la inmobiliaria INCAIBO, a los {compra.fecha.day} días del mes número {compra.fecha.month} del año {compra.fecha.year}.</b>", ParagraphStyle("", alignment=TA_CENTER)))
    
    return t

def reporte_compras(compras):
    t = []
    tabla = [['NÚM.', 'INMUEBLE', 'FECHA', 'ESTADO', 'PRECIO']]

    for compra in compras:
        tabla.append([Paragraph(str(compra.pk)), Paragraph(compra.inmueble.nombre),
                      Paragraph(str(compra.fecha.date())), Paragraph(compra.estado_largo()),
                      Paragraph(f"$ {compra.inmueble.precio}")])

    t.append(Table(tabla, colWidths=[0.5*inch, 3*inch, 1*inch, 1.5*inch, 1*inch]))

    return t

def reporte_pagos(request, pagos):
    t = []
    compra = Compra.objects.get(pk=request.resolver_match.kwargs['pk'])
    t.append(Table([['NÚMERO COMPRA', 'INMUEBLE', 'FECHA DE COMPRA', 'ESTADO', 'PRECIO'],
            [Paragraph(str(compra.pk)), Paragraph(compra.inmueble.nombre),
             Paragraph(str(compra.fecha.date())), Paragraph(compra.estado_largo()), Paragraph(f'${compra.inmueble.precio}')]]))
    
    t.append(Spacer(0,10))
    
    tabla = [['#', 'REFERENCIA', 'BANCO', 'FECHA', 'ESTADO', 'MONTO BS', 'MONTO $']]

    total_bs, total_dolar = 0, 0
    for (i,pago) in enumerate(pagos):
        tabla.append([str(i+1), Paragraph(str(pago.referencia)), Paragraph(str(pago.cuenta)), 
                      Paragraph(str(pago.fecha.date())), Paragraph(pago.estado_largo()),
                      Paragraph(f'Bs. {pago.monto}'), Paragraph(f'$ {round(pago.valor_dolar(),2)}')])
        
        if(pago.estado == 'A'):
            total_bs += pago.monto
            total_dolar += pago.valor_dolar()

    t.append(Table(tabla, colWidths=[0.5*inch,1*inch,2*inch,1*inch,1*inch,1*inch,1*inch]))
    t.append(Table([['','','','','',Paragraph(f"Bs.{total_bs}"),Paragraph(f"${round(total_dolar, 2)}")]], 
                   colWidths=[0.5*inch,1*inch,2*inch,1*inch,1*inch,1*inch,1*inch]))

    return t

def reporte_publicacion(inmueble):
    t, tabla = [], []

    try:
        imagen = Image('.' + inmueble.imagenes()[0],4*inch, 3*inch)
        t.append(imagen)
    except:
        print("No se pudo añadir imagen al PDF.")

    t.append(Paragraph(f'<b>PUBLICACIÓN DEL INMUEBLE <br></br>"{inmueble.nombre}"</b>',ParagraphStyle("", alignment=TA_CENTER, fontSize=16)))
    t.append(Spacer(0,15))
    tabla.append(['CAMPO', 'VALOR'])
    tabla.append(['PRECIO', Paragraph(f"${inmueble.precio}")])
    tabla.append(['PARROQUIA', Paragraph(f"{inmueble.sector.parroquia.nombre}")])
    tabla.append(['SECTOR', Paragraph(f"{inmueble.sector.nombre}")])
    tabla.append(['UBICACIÓN DETALLADA', Paragraph(f"{inmueble.ubicacion_detallada}")])
    tabla.append(['AÑO DE CONSTRUCCIÓN', Paragraph(f"{inmueble.ano_construccion}")])
    tabla.append(['TIPO DE CONSTRUCCIÓN', Paragraph(f"{inmueble.tipo_construccion}")])
    tabla.append(['TAMAÑO', Paragraph(f"{inmueble.tamano} m2.")])
    tabla.append(['NÚMERO DE HABITACIONES', Paragraph(f"{inmueble.habitaciones}")])
    tabla.append(['NÚMERO DE BAÑOS', Paragraph(f"{inmueble.banos}")])
    tabla.append(['NÚMERO DE PISOS', Paragraph(f"{inmueble.pisos}")])
    tabla.append(['PUESTOS DE ESTACIONAMIENTO', Paragraph(f"{inmueble.estacionamientos}")])
    tabla.append(['SERVICIO DE AGUA', Paragraph("SÍ" if inmueble.agua else "NO")])
    tabla.append(['SERVICIO DE ELECTRICIDAD', Paragraph("SÍ" if inmueble.electricidad else "NO")])
    tabla.append(['SERVICIO DE GAS', Paragraph("SÍ" if inmueble.gas else "NO")])
    tabla.append(['SERVICIO DE ASEO URBANO', Paragraph("SÍ" if inmueble.aseo else "NO")])
    tabla.append(['SERVICIO DE INTERNET', Paragraph("SÍ" if inmueble.internet else "NO")])

    t.append(Table(tabla, colWidths=(2.5*inch, 4.5*inch)))

    return t

def reporte_cita_formalidades(cita):
    t = []

    t.append(Paragraph("DATOS DE LA CITA FINAL", ParagraphStyle("", alignment=TA_CENTER, fontSize=16)))
    t.append(Spacer(0,10))

    t.append(Table([["DÍA", "HORA"], [f"{cita.fecha_asignada.date()}", f"{cita.fecha_asignada.hour}:00"]]))
    t.append(Spacer(0,10))

    t.append(Paragraph("DATOS DE LOS PAGOS REALIZADOS", ParagraphStyle("", alignment=TA_CENTER, fontSize=16)))
    t.append(Spacer(0,10))

    t.append(Table([["PAGO", "MONTO"], 
        ["MONTO PAGADO POR EL CLIENTE", f"${cita.compra.monto_cancelado()}"],
        ["COMISIÓN DE LA INMOBILIARIA", f"${cita.compra.comision_inmobiliaria()}"],
        ["IVA", f"${cita.compra.iva()}"],
        ["EXCEDENTE", f"${cita.compra.excedente()}"],
        ["COMISIÓN DUEÑO", f"{cita.compra.comision_dueno()}"]
    ]))

    return t