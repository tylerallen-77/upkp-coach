'use client'
import {useEffect,useState} from 'react'
import {api,pct,sec} from '../lib/api'
import QuestionRunner from '../components/QuestionRunner'

type Track='tpa'|'substansi'
const nav=[['home','Beranda'],['learn','Belajar'],['tryout','Try Out'],['progress','Progress'],['account','Account']]

export default function Page(){
 const [me,setMe]=useState<any>(null),[authMode,setAuthMode]=useState<'login'|'register'>('login'),[auth,setAuth]=useState({username:'',password:'',accept_terms:false}),[err,setErr]=useState('')
 const [view,setView]=useState('home'),[home,setHome]=useState<any>(null),[track,setTrack]=useState<Track>('tpa'),[catalog,setCatalog]=useState<any[]>([]),[bundle,setBundle]=useState<any>(null),[pm,setPm]=useState<any>(null),[progress,setProgress]=useState<any>(null),[busy,setBusy]=useState(false),[busyKey,setBusyKey]=useState(''),[actionErr,setActionErr]=useState(''),[mobileMenu,setMobileMenu]=useState(false)
 async function loadMe(){try{
   const d=await api('/api/auth/me');setMe(d.user);await loadHome()
   if(typeof window!=='undefined'){
     const raw=localStorage.getItem('upkp_active_bundle')
     if(raw){try{const saved=JSON.parse(raw);if(saved?.session?.id){setBundle(saved);setTrack(saved.session.track||'tpa');setView(saved.mode==='tryout'?'tryout':'learn')}}catch{}}
   }
 }catch{setMe(null)}}
 async function loadHome(){setHome(await api('/api/home'))}
 async function loadCatalog(t:Track){const d=await api('/api/catalog?track='+t);setCatalog(d.chapters||[])}
 async function loadProgress(t:Track){setProgress(await api('/api/progress?track='+t))}
 useEffect(()=>{loadMe()},[])
 useEffect(()=>{if(me){loadCatalog(track);loadProgress(track)}},[me,track])
 useEffect(()=>{if(!bundle)return;const h=(e:BeforeUnloadEvent)=>{e.preventDefault();e.returnValue=''};window.addEventListener('beforeunload',h);return()=>window.removeEventListener('beforeunload',h)},[bundle])
 async function doAuth(e:any){e.preventDefault();setErr('');setBusy(true);try{const d=await api('/api/auth/'+authMode,{method:'POST',body:JSON.stringify(auth)});setMe(d.user);await loadHome()}catch(e:any){setErr(e.message)}finally{setBusy(false)}}
 async function logout(){
   if(bundle){window.alert('Pause atau selesaikan sesi aktif terlebih dahulu.');return}
   await api('/api/auth/logout',{method:'POST'});setMobileMenu(false);setMe(null);setHome(null)
 }
 function rememberBundle(d:any){setBundle(d);if(typeof window!=='undefined')localStorage.setItem('upkp_active_bundle',JSON.stringify(d))}
 function clearBundle(){setBundle(null);if(typeof window!=='undefined')localStorage.removeItem('upkp_active_bundle')}
 async function startGuided(t:Track){setBusy(true);setBusyKey('guided:'+t);setPm(null);setActionErr('');try{const d=await api('/api/session/guided?track='+t,{method:'POST'});rememberBundle(d);setTrack(t);setView('learn')}catch(e:any){setActionErr(e.message||'Gagal menyiapkan sesi. Coba lagi.')}finally{setBusy(false);setBusyKey('')}}
 async function startChapter(code:string){setBusy(true);setBusyKey('chapter:'+code);setPm(null);setActionErr('');try{const d=await api('/api/session/chapter?code='+encodeURIComponent(code)+'&n=10&level=0',{method:'POST'});rememberBundle(d);setView('learn')}catch(e:any){setActionErr(e.message||'Gagal menyiapkan drill.')}finally{setBusy(false);setBusyKey('')}}
 async function startTryout(t:Track){setBusy(true);setBusyKey('tryout:'+t);setPm(null);setActionErr('');try{const d=await api('/api/session/tryout?track='+t,{method:'POST'});rememberBundle(d);setTrack(t);setView('tryout')}catch(e:any){setActionErr(e.message||'Gagal menyiapkan Try Out.')}finally{setBusy(false);setBusyKey('')}}
 async function startMastery(section:string,t:Track=track){setBusy(true);setBusyKey('mastery:'+section);setPm(null);setActionErr('');try{const d=await api('/api/session/mastery?track='+t+'&section='+encodeURIComponent(section),{method:'POST'});rememberBundle(d);setTrack(t);setView('progress')}catch(e:any){setActionErr(e.message||'Mastery Challenge belum bisa dimulai.')}finally{setBusy(false);setBusyKey('')}}
 async function sessionDone(x:any){
   if(bundle?.session?.id&&typeof window!=='undefined')localStorage.removeItem('upkp_paused_bundle_'+bundle.session.id)
   clearBundle();setPm(x);await loadHome();await loadProgress(track)
 }
 async function sessionExited(){
   if(bundle?.session?.id&&typeof window!=='undefined')localStorage.setItem('upkp_paused_bundle_'+bundle.session.id,JSON.stringify(bundle))
   clearBundle();setPm(null);setView('home');await loadHome();await loadProgress(track)
 }
 async function resumeSession(sid:string){
   setBusy(true);setBusyKey('resume:'+sid);setActionErr('')
   try{
     const local=typeof window!=='undefined'?localStorage.getItem('upkp_paused_bundle_'+sid):null
     const d=local?JSON.parse(local):await api('/api/session/resume/'+encodeURIComponent(sid),{method:'POST'})
     rememberBundle(d);setTrack(d.session.track||'tpa');setView(d.mode==='tryout'?'tryout':'learn')
   }catch(e:any){setActionErr(e.message||'Sesi tidak dapat dilanjutkan.')}
   finally{setBusy(false);setBusyKey('')}
 }
 async function navigate(id:string){
   if(bundle){window.alert('Masih ada sesi aktif. Gunakan tombol “Keluar sesi” di atas soal agar progress parsial tersimpan.');return}
   setView(id);setPm(null);setMobileMenu(false)
 }
 if(!me)return <main className="authShell"><section className="authBrand"><div className="logoBig">UPKP <span>Coach</span></div><h1>Belajar sampai terasa siap.</h1><p>Coach adaptif yang belajar dari pola jawabanmu dan mengarahkan latihan ke bagian yang paling perlu diperbaiki.</p><div className="authBullets"><span>✓ Guided learning</span><span>✓ Mastery badges</span><span>✓ TPA + Substansi</span></div></section><section className="authCard"><div className="seg"><button className={authMode==='login'?'active':''} onClick={()=>setAuthMode('login')}>Masuk</button><button className={authMode==='register'?'active':''} onClick={()=>setAuthMode('register')}>Buat akun</button></div><h2>{authMode==='login'?'Selamat datang lagi':'Mulai belajar'}</h2><form onSubmit={doAuth}><label>Username<input value={auth.username} onChange={e=>setAuth({...auth,username:e.target.value.toLowerCase()})} placeholder="rio_monanda" autoComplete="username"/></label><label>Password<input type="password" value={auth.password} onChange={e=>setAuth({...auth,password:e.target.value})} autoComplete={authMode==='login'?'current-password':'new-password'}/></label>{authMode==='register'&&<label className="termsCheck"><input type="checkbox" checked={auth.accept_terms} onChange={e=>setAuth({...auth,accept_terms:e.target.checked})}/><span>Saya setuju dengan <a href="/about" target="_blank">Ketentuan</a> dan <a href="/privacy" target="_blank">Privasi</a>.</span></label>}{err&&<div className="errorBox">{err}</div>}<button className="btn primary full" disabled={busy||(authMode==='register'&&!auth.accept_terms)}>{busy?'Memproses…':authMode==='login'?'Masuk':'Buat akun'}</button></form><p className="helper">Tanpa email atau OTP. Password recovery dibantu admin.</p><p className="helper"><a href="/about">Tentang & disclaimer</a> · <a href="/privacy">Privasi</a></p></section></main>
 return <div className="shell"><aside className="sidebar"><div><div className="brand">UPKP <span>Coach</span></div><div className="nav">{nav.map(([id,label])=><button key={id} className={view===id?'active':''} onClick={()=>navigate(id)}>{label}</button>)}</div></div><div className="userBox"><b>@{me.username}</b><small>{me.role==='admin'?'Admin':'Learner'}</small>{me.role==='admin'&&<a href="/admin" style={{color:'#ffd23f',fontSize:12,display:'block',marginBottom:8}}>Admin Console</a>}<button onClick={logout}>Keluar</button><small><a href="/about">Disclaimer</a> · <a href="/privacy">Privasi</a></small></div></aside><main className="content">{actionErr&&<div className="actionError"><span>{actionErr}</span><button onClick={()=>setActionErr('')}>×</button></div>}<header className="mobileHeader"><div className="brand">UPKP <span>Coach</span></div><button className="menuButton" aria-label="Buka menu" onClick={()=>setMobileMenu(true)}>☰</button></header>{mobileMenu&&<><button className="drawerBackdrop" aria-label="Tutup menu" onClick={()=>setMobileMenu(false)}/><aside className="mobileDrawer"><div className="drawerTop"><div className="brand">UPKP <span>Coach</span></div><button onClick={()=>setMobileMenu(false)}>×</button></div><div className="drawerNav">{nav.map(([id,label])=><button key={id} className={view===id?'active':''} onClick={()=>navigate(id)}>{label}</button>)}</div><div className="drawerAccount"><b>@{me.username}</b><small>{me.role==='admin'?'Admin':'Learner'}</small>{me.role==='admin'&&<a href="/admin">Admin Console</a>}<a href="/about">Tentang & disclaimer</a><a href="/privacy">Privasi</a><button className="drawerLogout" onClick={logout}>Keluar</button></div></aside></>}
 {view==='home'&&<Home data={home} busy={busy} busyKey={busyKey} start={startGuided} resume={resumeSession}/>}
 {view==='learn'&&<Learn track={track} setTrack={setTrack} catalog={catalog} bundle={bundle} pm={pm} startGuided={startGuided} startChapter={startChapter} onDone={sessionDone} onExit={sessionExited} busy={busy}/>}
 {view==='tryout'&&<TryOut track={track} setTrack={setTrack} bundle={bundle} pm={pm} start={startTryout} onDone={sessionDone} onExit={sessionExited} busy={busy}/>}
 {view==='progress'&&<Progress track={track} setTrack={setTrack} data={progress} bundle={bundle} pm={pm} startMastery={startMastery} onDone={sessionDone} onExit={sessionExited} busy={busy}/>}
 {view==='account'&&<Account me={me} onReset={async()=>{clearBundle();if(typeof window!=='undefined'){Object.keys(localStorage).filter(k=>k.startsWith('upkp_runner_')||k.startsWith('upkp_paused_bundle_')).forEach(k=>localStorage.removeItem(k))}await loadHome();await loadProgress(track)}}/>}
 </main></div>
}

function TrackTabs({track,setTrack}:{track:Track,setTrack:(t:Track)=>void}){return <div className="trackTabs"><button className={track==='tpa'?'active':''} onClick={()=>setTrack('tpa')}>TPA</button><button className={track==='substansi'?'active':''} onClick={()=>setTrack('substansi')}>Substansi β</button></div>}

function Home({data,busy,busyKey,start,resume}:any){
 if(!data)return <div className="loading">Memuat coach…</div>
 const tpa=data.tracks.find((x:any)=>x.track==='tpa'),sub=data.tracks.find((x:any)=>x.track==='substansi')
 const mastery=tpa?.mastery,subMastery=sub?.mastery
 const totalEarned=(mastery?.earned||0)+(subMastery?.earned||0),totalBadges=(mastery?.total||0)+(subMastery?.total||0)
 return <><div className="hero"><div><div className="eyebrow">TODAY'S PLAN</div><h1>Halo, {data.user.username}.</h1><p>Targetmu sederhana: ikuti latihan hari ini dan kumpulkan semua Mastery Badge sebelum UPKP.</p></div></div>
 {(mastery||subMastery)&&<section className={'masteryHero '+(mastery?.tpa_ready&&subMastery?.substansi_ready?'ready':'')}><div><span className="eyebrow">UPKP READINESS</span><h2>{mastery?.tpa_ready&&subMastery?.substansi_ready?'UPKP Ready ✓':`${totalEarned} / ${totalBadges} badge mastered`}</h2><p>Target akhir: tuntaskan TPA dan Substansi. Coach menjaga kedua track tetap seimbang sampai seluruh badge terpenuhi.</p></div><div className="badgeStrip"><div className={'miniBadge '+(mastery?.tpa_ready?'earned':'')}><span>{mastery?.tpa_ready?'✓':'◔'}</span><small>TPA</small><b>{mastery?.earned||0}/{mastery?.total||4}</b></div><div className={'miniBadge '+(subMastery?.substansi_ready?'earned':'')}><span>{subMastery?.substansi_ready?'✓':'◔'}</span><small>Substansi</small><b>{subMastery?.earned||0}/{subMastery?.total||6}</b></div></div></section>}
 {data.active_sessions?.length>0&&<section className="panel activeSessions"><div className="sectionTitle"><div><span className="pill">PAUSED</span><h3>Lanjutkan sesi</h3></div></div>{data.active_sessions.map((x:any)=><div className="row" key={x.id}><div><b>{x.title}</b><small>{x.track==='tpa'?'TPA':'Substansi'} · mulai {new Date(x.started*1000).toLocaleString('id-ID')}</small></div><button className="btn primary compact" disabled={busy} onClick={()=>resume(x.id)}>{busyKey==='resume:'+x.id?'Membuka…':'Lanjutkan'}</button></div>)}</section>}
 <div className="homeTracks"><TodayCard t={tpa} busy={busyKey==='guided:tpa'} start={start}/><TodayCard t={sub} busy={busyKey==='guided:substansi'} start={start}/></div>
 <section className="panel recent"><h3>Sesi terakhir</h3>{data.sessions?.length?data.sessions.map((s:any)=><div className="row" key={s.id}><div><b>{s.title}</b><small>{s.track==='tpa'?'TPA':'Substansi'} · {new Date(s.started*1000).toLocaleString('id-ID')}</small></div><span>{s.summary?.accuracy!=null?pct(s.summary.accuracy):'—'}</span></div>):<p className="muted">Belum ada sesi.</p>}</section></>
}
function TodayCard({t,busy,start}:any){if(!t)return null;return <section className="trackCard"><div className="trackHead"><div><span className="pill">{t.track==='tpa'?'TPA':'SUBSTANSI · BETA'}</span><h2>{t.track==='tpa'?'Latihan TPA hari ini':'Substansi hari ini'}</h2></div><div className="readiness"><b>{t.metrics.readiness||0}</b><small>readiness</small></div></div><p className="coachCopy">{t.prescription.summary}</p><div className="planLines">{t.prescription.items.slice(0,3).map((x:any,i:number)=><div key={i}><span>{x.label}</span><small>{x.questions} soal · ±{x.minutes}m</small></div>)}</div><button className="btn primary full" disabled={busy} onClick={()=>start(t.track)}>{busy?'Menyiapkan sesi…':(t.metrics.n?'Mulai rencana hari ini':'Mulai diagnostic →')}</button></section>}

function Learn({track,setTrack,catalog,bundle,pm,startGuided,startChapter,onDone,onExit,busy}:any){
 if(bundle)return <QuestionRunner bundle={bundle} onDone={onDone} onExit={onExit}/>
 return <><div className="pageHead"><div><div className="eyebrow">BELAJAR</div><h1>Coach yang memilih arah utama.</h1><p>Kamu cukup mulai dari sesi rekomendasi. Materi per bab tersedia kalau ingin memahami pola atau shortcut tertentu.</p></div><TrackTabs track={track} setTrack={setTrack}/></div>{pm&&<PostMortem pm={pm}/>}
 <section className="guidedCard"><div><span className="pill">RECOMMENDED</span><h2>Today's guided session</h2><p>Weakness drill + review jatuh tempo + maintenance area yang sudah kuat.</p></div><button className="btn primary" disabled={busy} onClick={()=>startGuided(track)}>{busy?'Menyiapkan…':'Mulai →'}</button></section>
 <div className="chapters">{catalog.map((c:any)=><details className="chapter" key={c.code}><summary><div><b>{c.title}</b><small>{c.subtest}</small></div><span>＋</span></summary><div className="chapterBody"><div className="material">{c.material||'Materi ringkas belum tersedia.'}</div><div className="sourceNote">Basis: {c.source_note}</div>{c.source_refs?.length>0&&<div className="sourceRefs">{c.source_refs.map((s:any)=><a key={s.url} href={s.url} target="_blank" rel="noreferrer">{s.name}</a>)}</div>}<button className="btn ghost" onClick={()=>startChapter(c.code)}>Drill bab ini</button></div></details>)}</div></>
}

function TryOut({track,setTrack,bundle,pm,start,onDone,onExit,busy}:any){if(bundle)return <QuestionRunner bundle={bundle} onDone={onDone} onExit={onExit}/>;return <><div className="pageHead"><div><div className="eyebrow">TRY OUT</div><h1>Simulasikan kondisi ujian.</h1><p>Feedback ditahan sampai selesai. Gunakan pass pertama untuk mengamankan cheap points.</p></div><TrackTabs track={track} setTrack={setTrack}/></div>{pm&&<PostMortem pm={pm}/>}<section className="tryCard"><div className="tryIcon">◎</div><div><span className="pill">3-PASS STRATEGY</span><h2>{track==='tpa'?'Try Out Tes Potensi':'Try Out Substansi Kemenkeu'}</h2><p>Hasil try out ikut memengaruhi model kemampuanmu.</p></div><button className="btn primary" disabled={busy} onClick={()=>start(track)}>{busy?'Menyiapkan…':'Mulai Try Out'}</button></section></>}

function Progress({track,setTrack,data,bundle,pm,startMastery,onDone,onExit,busy}:any){
 if(bundle)return <QuestionRunner bundle={bundle} onDone={onDone} onExit={onExit}/>
 const badges=data?.snapshot?.mastery?.badges||[]
 return <><div className="pageHead"><div><div className="eyebrow">PROGRESS</div><h1>Mastery, bukan sekadar jumlah soal.</h1><p>{track==='tpa'?'TPA menilai coverage, difficulty, speed, retention, dan Mastery Challenge.':'Substansi menilai coverage, akurasi, retention, Exam-level evidence, dan Mastery Challenge.'}</p></div><TrackTabs track={track} setTrack={setTrack}/></div>{pm&&<PostMortem pm={pm}/>}
 {!data?<div className="loading">Memuat…</div>:<><section className="badgeGrid">{badges.map((b:any)=><article className={'masteryBadge '+(b.earned?'earned':'')} key={b.section}><div className="badgeIcon">{b.earned?'✓':'◔'}</div><div><span className="eyebrow">{b.earned?'MASTERED':'IN PROGRESS'}</span><h3>{b.label}</h3><div className="badgeProgress"><i style={{width:b.progress+'%'}}/></div><p>{b.progress}% · Exam accuracy {pct(b.exam_accuracy||0)} · {b.exam_attempts} Exam-level attempts{track==='substansi'&&b.retention?' · retention ✓':''}</p>{b.earned?<div className="badgeEarned">Badge earned</div>:b.challenge_unlocked?<button className="btn primary" onClick={()=>startMastery(b.section,track)}>Ambil Mastery Challenge</button>:<small className="muted">Challenge terbuka setelah coverage, retention, dan Exam-level gate terpenuhi.</small>}</div></article>)}</section>
 <div className="metricGrid"><Metric label="Readiness" v={data.snapshot.metrics.readiness||0}/><Metric label="Akurasi last 50" v={pct(data.snapshot.metrics.accuracy)}/><Metric label="Median" v={sec(data.snapshot.metrics.median_ms)}/><Metric label="Mastered micro-skill" v={(data.snapshot.metrics.mastered||0)+' / '+(data.snapshot.metrics.skills||0)}/></div>
 <section className="panel"><h3>Skill map</h3><div className="skillTable"><div className="skillRow head"><span>Skill</span><span>Akurasi</span><span>Median</span><span>Status</span></div>{data.skills.map((s:any)=><div className="skillRow" key={s.skill}><span><b>{s.label}</b><small>{s.n} attempt · recommended {difficulty(s.recommended_level)}</small></span><span>{pct(s.accuracy)}</span><span>{sec(s.median_ms)}</span><span className={'state '+s.state.toLowerCase()}>{s.state}</span></div>)}</div></section></>}</>
}
function Account({me,onReset}:any){
 return <><div className="pageHead"><div><div className="eyebrow">ACCOUNT</div><h1>Akun & data.</h1><p>Kelola akun tanpa mencampurkannya dengan learning progress.</p></div></div>
 <section className="panel accountCard"><h3>@{me.username}</h3><p className="muted">{me.role==='admin'?'Administrator':'Learner'}</p>{me.role==='admin'&&<p><a className="btn primary accountLink" href="/admin">Buka Admin Console →</a></p>}</section>
 <section className="panel"><h3>Reset Riwayat Pembelajaran</h3><p className="muted">Menghapus attempts, sesi, progress, readiness, review state, dan Mastery Badge. Username, password, dan akun tetap ada.</p><button className="btn ghost danger" onClick={async()=>{const pw=window.prompt('Masukkan password untuk reset riwayat pembelajaran');if(!pw)return;if(!window.confirm('Reset seluruh riwayat belajar dan mastery? Akun tetap dipertahankan.'))return;try{await api('/api/account/reset-learning',{method:'POST',body:JSON.stringify({password:pw})});await onReset();window.alert('Riwayat pembelajaran sudah direset.')}catch(e:any){window.alert(e.message)}}}>Reset Riwayat Pembelajaran</button></section>
 <section className="panel"><h3>Hapus Akun</h3><p className="muted">Menghapus akun beserta seluruh data secara permanen.</p><button className="btn ghost danger" onClick={async()=>{const pw=window.prompt('Masukkan password untuk menghapus akun secara permanen');if(!pw)return;if(!window.confirm('Hapus akun dan seluruh data? Tindakan ini tidak dapat dibatalkan.'))return;try{await api('/api/account/delete',{method:'POST',body:JSON.stringify({password:pw})});window.location.href='/'}catch(e:any){window.alert(e.message)}}}>Hapus akun saya</button></section>
 <section className="panel accountLinks"><a href="/about">Tentang & disclaimer</a><a href="/privacy">Privasi</a></section></>
}

function difficulty(n:number){return ({1:'Foundation',2:'Standard',3:'Exam',4:'Hard',5:'Expert'} as any)[n]||'Standard'}
function Metric({label,v}:{label:string,v:any}){return <div className="metric"><small>{label}</small><b>{v}</b></div>}
function PostMortem({pm}:{pm:any}){return <section className="post"><b>{pm.mastery_passed?'Mastery Challenge PASS ✓':pm.section&&pm.mastery_passed===false?'Mastery Challenge belum lolos':`Sesi selesai · ${pm.correct}/${pm.n} benar`}</b><span>{pct(pm.accuracy)} · median {sec(pm.median_ms)}</span><p>{pm.recommendation|| (pm.mastery_passed?'Badge akan diperbarui di halaman Progress.':'Coach akan memasukkan area yang belum kuat ke latihan berikutnya.')}</p></section>}
