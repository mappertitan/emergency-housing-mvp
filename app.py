import json, uuid
from datetime import datetime, timedelta
from pathlib import Path
import folium
import streamlit as st
from folium.plugins import Fullscreen
from PIL import Image, ImageDraw, ImageFont
from streamlit_folium import st_folium

APP_DIR=Path(__file__).resolve().parent
DATA_DIR=APP_DIR/'data'; PHOTO_DIR=APP_DIR/'photos'; REPORT_DIR=APP_DIR/'reports'
for p in (DATA_DIR,PHOTO_DIR,REPORT_DIR): p.mkdir(exist_ok=True)
DB_FILE=DATA_DIR/'cases.json'

st.set_page_config(page_title='Emergency Housing — MVP 0.4',page_icon='🏠',layout='wide',initial_sidebar_state='collapsed')
#st.markdown('''<style>.stApp{background:linear-gradient(135deg,#07111f 0%,#0d1c2f 55%,#13263c 100%)}.block-container{max-width:1400px;padding-top:1rem}.hero{padding:25px 28px;border-radius:22px;color:white;background:linear-gradient(120deg,#10234a,#172f58 55%,#1c5a47);border:1px solid rgba(255,255,255,.12)}.hero h1{margin:0;font-size:2.15rem}.hero p{color:#dce7f5;margin-top:.4rem}.card{background:rgba(13,23,36,.88);border:1px solid rgba(255,255,255,.10);border-radius:18px;padding:18px;margin-bottom:14px;color:#eef4fb}.small{color:#aebed1;font-size:.88rem}.badge{display:inline-block;padding:5px 11px;border-radius:999px;font-weight:700}.high{background:#5b1f23;color:#ffb7b5}.medium{background:#59420e;color:#ffd77a}.low{background:#153f26;color:#9be7a9}</style>''',unsafe_allow_html=True)

st.markdown('''<style>
/* =========================================================
   EMERGENCY HOUSING — GLOBAL UI
   ========================================================= */

.stApp{
    background:linear-gradient(135deg,#07111f 0%,#0d1c2f 55%,#13263c 100%)
}

.block-container{
    max-width:1400px;
    padding-top:1rem
}

/* =========================================================
   HERO
   ========================================================= */

.hero{
    padding:25px 28px;
    border-radius:22px;
    color:#ffffff;
    background:linear-gradient(120deg,#10234a,#172f58 55%,#1c5a47);
    border:1px solid rgba(255,255,255,.12)
}

.hero h1{
    margin:0;
    font-size:2.15rem
}

.hero p{
    color:#dce7f5;
    margin-top:.4rem
}

/* =========================================================
   CARDS
   ========================================================= */

.card{
    background:#111827;
    border:1px solid #263244;
    border-radius:18px;
    padding:20px;
    margin-bottom:16px;
    color:#f3f4f6;
    box-shadow:0 4px 14px rgba(0,0,0,.18)
}

.card p{
    color:#cbd5e1;
}

.card-title{
    color:#f8fafc;
    font-size:1.05rem;
    font-weight:700;
    margin-bottom:6px;
}

.card-subtitle{
    color:#cbd5e1;
    font-size:.90rem;
    line-height:1.5;
}

/* =========================================================
   SMALL / SECONDARY TEXT
   ========================================================= */

.small{
    color:#cbd5e1;
    font-size:.88rem;
    line-height:1.5
}

/* =========================================================
   BADGES / PRIORITY
   ========================================================= */

.badge{
    display:inline-block;
    padding:5px 11px;
    border-radius:999px;
    font-weight:700
}

.high{
    background:#5b1f23;
    color:#ffb7b5
}

.medium{
    background:#59420e;
    color:#ffd77a
}

.low{
    background:#153f26;
    color:#9be7a9
}

/* =========================================================
   FORM ELEMENTS — CONTRAST
   ========================================================= */

label{
    color:#f3f4f6 !important;
}

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stRadio label,
.stCheckbox label,
.stFileUploader label,
.stTextArea label{
    color:#f3f4f6 !important;
}

.stMarkdown p{
    color:#dbe5f0;
}

/* Texto de ayuda debajo de los widgets */
.stTextInput small,
.stNumberInput small,
.stSelectbox small,
.stRadio small,
.stFileUploader small{
    color:#aebed1 !important;
}

/* =========================================================
   INPUTS
   ========================================================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea{
    background-color:#0f172a !important;
    color:#f3f4f6 !important;
    border:1px solid #334155 !important;
}

.stTextInput input::placeholder,
.stNumberInput input::placeholder,
.stTextArea textarea::placeholder{
    color:#94a3b8 !important;
}

/* =========================================================
   RADIO / CHECKBOX TEXT
   ========================================================= */

.stRadio label,
.stCheckbox label{
    color:#e5edf7 !important;
}

/* =========================================================
   BUTTONS
   ========================================================= */

.stButton button{
    border-radius:10px;
    font-weight:600;
}

/* =========================================================
   TRIAGE
   ========================================================= */

.eh-triage{
    background:#172033;
    border:1px solid #334155;
    border-radius:14px;
    padding:22px;
    margin-top:20px;
}

.eh-triage-title{
    color:#f8fafc;
    font-size:1.1rem;
    font-weight:700;
}

.eh-triage-text{
    color:#cbd5e1;
    line-height:1.5;
}
.prototype-banner{
    background:#111827;
    border:1px solid #334155;
    border-left:5px solid #f59e0b;
    border-radius:14px;
    padding:14px 18px;
    margin-bottom:18px;
    color:#f3f4f6;
}

.prototype-title{
    font-weight:700;
    font-size:1rem;
    margin-bottom:4px;
}

.prototype-main{
    font-weight:600;
    font-size:.95rem;
    margin-bottom:4px;
}

.prototype-sub{
    color:#cbd5e1;
    font-size:.82rem;
    line-height:1.4;
}

</style>''',unsafe_allow_html=True)
# ⚠️ RESEARCH PROTOTYPE #Message to public. 
st.markdown("""
<div class="prototype-banner">
    <div class="prototype-title">
        ⚠️ Research prototype
    </div>
    <div class="prototype-main">
        Please do not submit real personal, property or emergency information.
    </div>
    <div class="prototype-sub">
        This prototype is for demonstration and research purposes only.
        It does not replace professional structural inspection,
        official damage assessment, or emergency services.
    </div>
</div>
""", unsafe_allow_html=True)

QUESTIONS=[('structural','¿Observas grietas importantes, columnas o vigas dañadas, o elementos estructurales deformados?'),('partial_collapse','¿Hay colapso parcial de techo, piso, muro o una parte importante de la vivienda?'),('total_collapse','¿La vivienda presenta colapso total o una parte importante está completamente en escombros?'),('instability','¿Observas inclinación, desplazamiento o movimiento visible de la estructura?'),('debris','¿Hay grandes cantidades de escombros o elementos que hayan caído dentro de la vivienda?'),('utilities','¿Hay fugas, cables expuestos, fuego, olor a gas u otro peligro visible?'),('access','¿La entrada, las escaleras o las rutas de salida están bloqueadas o dañadas?'),('occupancy','¿La vivienda estaba ocupada cuando ocurrió el terremoto?'),('dependent','¿En la vivienda viven niños pequeños, adultos mayores o personas con movilidad reducida?'),('uninhabitable','¿Por el estado observado, consideras que no es seguro permanecer dentro de la vivienda?')]
DEMO_CASES=[{'id':'DEMO-240381','lat':3.4516,'lon':-76.5320,'priority':'ALTA','score':88,'damage':'Colapso parcial'},{'id':'DEMO-571204','lat':3.4288,'lon':-76.5225,'priority':'MEDIA','score':61,'damage':'Daño estructural visible'},{'id':'DEMO-813625','lat':3.4742,'lon':-76.5091,'priority':'BAJA','score':29,'damage':'Daños menores'},{'id':'DEMO-905117','lat':3.4370,'lon':-76.5480,'priority':'ALTA','score':79,'damage':'Daño severo'}]

def load_cases():
    if not DB_FILE.exists(): return []
    try: return json.loads(DB_FILE.read_text(encoding='utf-8'))
    except Exception: return []

def save_cases(cases): DB_FILE.write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')

def calculate_priority(a):
    weights={'total_collapse':(45,'colapso total'),'partial_collapse':(30,'colapso parcial'),'structural':(25,'daño estructural visible'),'instability':(25,'inestabilidad o desplazamiento'),'utilities':(20,'peligro asociado a servicios'),'uninhabitable':(20,'vivienda reportada como no segura'),'debris':(12,'presencia importante de escombros'),'access':(10,'acceso o evacuación comprometidos'),'dependent':(10,'personas dependientes en la vivienda'),'occupancy':(5,'vivienda ocupada durante el evento')}
    score=0; reasons=[]
    for k,(w,r) in weights.items():
        if a.get(k): score+=w; reasons.append(r)
    score=min(score,100); priority='ALTA' if score>=70 else 'MEDIA' if score>=40 else 'BAJA'
    return score,priority,reasons

def appointment_slots():
    now=datetime.now().replace(minute=0,second=0,microsecond=0); out=[]
    for d in range(1,8):
        day=now+timedelta(days=d)
        for h in (8,10,14,16): out.append(day.replace(hour=h))
    return out

def create_png_report(c):
    W,H=1600,2100; img=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(img)
    fp='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bp='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    try: title=ImageFont.truetype(bp,52); head=ImageFont.truetype(bp,30); body=ImageFont.truetype(fp,25); small=ImageFont.truetype(fp,20)
    except Exception: title=head=body=small=None
    d.rectangle((0,0,W,230),fill='#10264d'); d.text((70,45),'EMERGENCY HOUSING',fill='white',font=title); d.text((72,125),'Pre-triage de vivienda — expediente preliminar',fill='#dce7f5',font=body)
    y=280
    for text,font,fill,dy in [(f"ID: {c['id']}",head,'#10264d',55),(f"Fecha/hora: {c['created_at']}",small,'#333',45),(f"Dirección: {c.get('address') or 'No indicada'}",body,'#333',45),(f"Coordenadas: {c['lat']:.6f}, {c['lon']:.6f}",small,'#333',70)]: d.text((70,y),text,fill=fill,font=font); y+=dy
    pc={'ALTA':'#8b2525','MEDIA':'#8b6a14','BAJA':'#1d6b3a'}[c['priority']]; d.rounded_rectangle((70,y,W-70,y+110),radius=22,fill=pc); d.text((105,y+18),f"PRIORIDAD PRELIMINAR: {c['priority']}",fill='white',font=head); d.text((105,y+65),f"Score heurístico: {c['score']}/100",fill='white',font=body); y+=155
    d.text((70,y),'Motivos de priorización',fill='#10264d',font=head); y+=50
    for r in c['reasons']: d.text((95,y),'• '+r,fill='#333',font=body); y+=38
    y+=20; d.text((70,y),'Visita profesional tentativa',fill='#10264d',font=head); y+=50; d.text((95,y),c.get('appointment','Pendiente'),fill='#333',font=body); y+=75
    d.text((70,y),'Alcance del expediente',fill='#10264d',font=head); y+=50
    d.multiline_text((95,y),'Este documento registra un reporte ciudadano y genera un pre-triage para ayudar a priorizar una visita técnica. No determina habitabilidad ni sustituye una evaluación profesional.',fill='#333',font=body,spacing=10)
    d.text((70,1500),f"Fotografías adjuntas: {c['photo_count']}",fill='#10264d',font=head); d.text((70,H-60),'Documento preliminar generado automáticamente.',fill='#777',font=small)
    out=REPORT_DIR/f"{c['id']}.png"; img.save(out,'PNG'); return out

def create_map(cases, location=None, zoom=14):
    center = location or [3.4516, -76.5320]
    m=folium.Map(location=center,zoom_start=zoom,tiles='OpenStreetMap',control_scale=True); Fullscreen(position='topright').add_to(m)
    demo=folium.FeatureGroup(name='🏠 Expedientes DEMO',show=True); real=folium.FeatureGroup(name='📋 Expedientes registrados',show=True)
    def col(p): return {'ALTA':'red','MEDIA':'orange','BAJA':'green'}.get(p,'blue')
    for c in DEMO_CASES:
        folium.Marker([c['lat'],c['lon']],tooltip=f"{c['id']} · {c['priority']}",popup=f"<b>{c['id']}</b><br>Prioridad: {c['priority']}<br>Score: {c['score']}<br>{c['damage']}",icon=folium.Icon(color=col(c['priority']),icon='home',prefix='fa')).add_to(demo)
    for c in cases:
        folium.Marker([c['lat'],c['lon']],tooltip=f"{c['id']} · {c['priority']}",popup=f"<b>{c['id']}</b><br>Prioridad preliminar: {c['priority']}<br>Score: {c['score']}<br>Dirección: {c.get('address') or 'No indicada'}<br>Visita: {c.get('appointment') or 'Pendiente'}",icon=folium.Icon(color=col(c['priority']),icon='home',prefix='fa')).add_to(real)
    demo.add_to(m); real.add_to(m); folium.LayerControl(collapsed=False).add_to(m); return m

if 'created_case' not in st.session_state: st.session_state.created_case=None
st.markdown('<div class="hero"><h1>🏠 Emergency Housing</h1><p>MVP 0.4 · Registro rápido de daños y pre-triage para priorizar una visita profesional</p></div>',unsafe_allow_html=True)
st.info('Acaba de ocurrir un terremoto. Es normal estar nervioso, tener miedo o no saber qué hacer. Si alguien puede estar atrapado, la prioridad es activar los servicios de emergencia. Esta aplicación no sustituye a bomberos, rescate ni a un profesional de estructuras. Su objetivo es dejar un registro rápido del estado de la vivienda y ayudar a organizar la visita técnica.')
tab_report,tab_map=st.tabs(['📝 Mi reporte','🗺️ Mapa operativo'])
with tab_report:
    st.markdown('<div class="card"><b>1. Localiza tu vivienda</b><br><span class="small">Puedes escribir la dirección y/o ubicar la vivienda directamente en el mapa. Haz clic sobre el punto aproximado de tu vivienda para registrar las coordenadas.</span></div>',unsafe_allow_html=True)

    if 'location_lat' not in st.session_state:
        st.session_state.location_lat = 3.451600
    if 'location_lon' not in st.session_state:
        st.session_state.location_lon = -76.532000

    location_map = folium.Map(
        location=[st.session_state.location_lat, st.session_state.location_lon],
        zoom_start=16,
        tiles='OpenStreetMap',
        control_scale=True,
    )
    folium.Marker(
        [st.session_state.location_lat, st.session_state.location_lon],
        tooltip='Ubicación seleccionada',
        icon=folium.Icon(color='blue', icon='home', prefix='fa'),
    ).add_to(location_map)

    map_result = st_folium(
        location_map,
        width=None,
        height=360,
        returned_objects=['last_clicked'],
        key='user_location_map',
    )

    clicked = map_result.get('last_clicked') if map_result else None
    if clicked:
        st.session_state.location_lat = float(clicked['lat'])
        st.session_state.location_lon = float(clicked['lng'])
        st.rerun()

    c1,c2=st.columns(2)
    with c1: lat=st.number_input('Latitud',key='location_lat',format='%.6f')
    with c2: lon=st.number_input('Longitud',key='location_lon',format='%.6f')
    address=st.text_input('Dirección de la vivienda',placeholder='Ej. Calle 10 # 20-30, Cali')
    st.caption('Mapa base: OpenStreetMap. El usuario puede seleccionar la ubicación manualmente; la dirección se conserva como campo independiente.')
    st.markdown('<div class="card"><b>2. Pre-triage de la vivienda</b><br><span class="small">No necesitas decidir tu propia prioridad. Las respuestas alimentan automáticamente un score transparente.</span></div>',unsafe_allow_html=True)
    answers={}
    for k,q in QUESTIONS:
        r=st.radio(q,['No','Sí','No puedo determinarlo'],horizontal=True,key=f'q_{k}'); answers[k]=(r=='Sí')
    score,priority,reasons=calculate_priority(answers); cls={'ALTA':'high','MEDIA':'medium','BAJA':'low'}[priority]
    st.markdown(f'<div class="card"><b>Pre-triage calculado</b><br><br><span class="badge {cls}">PRIORIDAD {priority}</span>&nbsp;&nbsp;Score: <b>{score}/100</b><br><br><span class="small">El score es heurístico y experimental. No es una evaluación estructural.</span></div>',unsafe_allow_html=True)
    st.markdown('<div class="card"><b>3. Evidencia fotográfica</b><br><span class="small">Añade entre 1 y 10 fotografías. No necesitas exponerte a ningún peligro para conseguirlas.</span></div>',unsafe_allow_html=True)
    uploads=st.file_uploader('Fotografías de la vivienda',type=['jpg','jpeg','png','webp'],accept_multiple_files=True); photos=uploads[:10] if uploads else []
    if photos:
        st.caption(f'{len(photos)} fotografía(s) seleccionada(s).'); cols=st.columns(min(5,len(photos)))
        for i,p in enumerate(photos): cols[i%len(cols)].image(p,caption=f'Foto {i+1}',use_container_width=True)
    st.markdown('<div class="card"><b>4. Visita profesional tentativa</b><br><span class="small">No es una cita confirmada. Es una ventana tentativa para la visita del profesional o institución encargada de la caracterización.</span></div>',unsafe_allow_html=True)
    appts=appointment_slots(); labels=[x.strftime('%d/%m/%Y — %H:%M') for x in appts]; appointment=st.selectbox('Selecciona una ventana tentativa',labels)
    st.markdown('<div class="card"><b>5. Si hay una persona atrapada</b><br><span class="small">Esta aplicación no registra víctimas. Debe utilizarse el canal oficial de emergencias habilitado durante el evento.</span></div>',unsafe_allow_html=True)
    emergency_url=st.text_input('Enlace oficial de emergencia',placeholder='Se configurará con la autoridad competente')
    if st.button('🚨 Generar expediente y registrar reporte',type='primary',use_container_width=True):
        if not photos: st.warning('Añade al menos una fotografía para crear el expediente.')
        else:
            case_id='EH-'+datetime.now().strftime('%y%m%d')+'-'+uuid.uuid4().hex[-6:].upper()
            case={'id':case_id,'created_at':datetime.now().strftime('%d/%m/%Y %H:%M'),'lat':float(lat),'lon':float(lon),'address':address.strip(),'answers':answers,'priority':priority,'score':score,'reasons':reasons,'appointment':appointment,'photo_count':len(photos),'emergency_url':emergency_url.strip()}
            cases=load_cases(); cases.append(case); save_cases(cases)
            for i,p in enumerate(photos,1):
                im=Image.open(p).convert('RGB'); im.save(PHOTO_DIR/f'{case_id}_{i:02d}.jpg','JPEG',quality=90)
            report=create_png_report(case); st.session_state.created_case=case; st.success(f'Expediente {case_id} registrado.')
            st.download_button('📄 Descargar expediente PNG',data=report.read_bytes(),file_name=report.name,mime='image/png',use_container_width=True)
    if st.session_state.created_case:
        c=st.session_state.created_case
        st.markdown(f'<div class="card"><b>Tu expediente</b><br><br>ID: <b>{c["id"]}</b><br>Prioridad preliminar: <b>{c["priority"]}</b> · Score: <b>{c["score"]}/100</b><br>Visita tentativa: <b>{c["appointment"]}</b><br><br><span class="small">Guarda el ID de tu expediente. La evaluación profesional sigue siendo necesaria.</span></div>',unsafe_allow_html=True)
with tab_map:
    st.markdown('<div class="card"><b>Mapa operativo</b><br><span class="small">Los expedientes DEMO y los expedientes reales están en capas independientes. Puedes activar o desactivar cada capa desde el control de capas.</span></div>',unsafe_allow_html=True)
    cases=load_cases(); st_folium(create_map(cases),width=None,height=650,returned_objects=[])
    st.markdown('### Expedientes reales registrados')
    if cases:
        data=[{'ID':c['id'],'Fecha':c['created_at'],'Prioridad':c['priority'],'Score':c['score'],'Dirección':c.get('address',''),'Lat':c['lat'],'Lon':c['lon'],'Visita tentativa':c.get('appointment','')} for c in cases]
        st.dataframe(data,use_container_width=True,hide_index=True)
    else: st.info('Todavía no hay expedientes reales. Los puntos DEMO se mantienen visibles.')
st.markdown('---'); st.caption('MVP 0.4 — prototipo de investigación. No es una certificación de habitabilidad, no sustituye una evaluación estructural y no sustituye los servicios oficiales de emergencia.')
